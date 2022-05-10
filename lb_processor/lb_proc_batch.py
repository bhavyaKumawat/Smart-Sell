import asyncio
import json
import logging
import os
from typing import Dict

from azure.servicebus import ServiceBusReceiveMode
from azure.servicebus.aio import ServiceBusClient
from azure.storage.blob.aio import BlobLeaseClient

from commons.msi_helper.msi_util import get_msi_cred
from commons.storage_helper.blob_msi_util import blob_exists, read_blob, write_sm_blob
from commons.utils import get_store_key, get_fran_key, get_loc_id, get_fran_emp_key
from lb_processor.helpers.fran_helper_batch import proc_store_rec_batch, create_fran_container_batch
from lb_processor.helpers.store_helper_batch import update_emp_rec_batch, create_emp_container_batch

logger = logging.getLogger('smartsell')

sb_ns_endpoint = 'sb://{0}.servicebus.windows.net'.format(os.environ['sb_ns_name'])

lb_queue_name = os.environ["lb_queue_name"]
container_name = os.environ["lb_container_name"]


async def process_sm_message(sm: Dict):
    store_key = get_store_key(sm[0])
    fran_key = get_fran_key(sm[0])
    loc_id = get_loc_id(sm[0])
    fran_emp_key = get_fran_emp_key(sm[0])
    rest_no = sm[0]["Rest_Number"]
    fran_id = sm[0]["FranchiseeId"]

    store_json = await perform_store_tran(store_key, sm)

    await asyncio.gather(
        perform_franchisee_tran(fran_key, loc_id, rest_no, fran_id, store_json),
        perform_emp_franchisee_tran(fran_emp_key, sm))


async def perform_store_tran(store_key: str, sm: Dict) -> Dict:
    store_json, lease, store_blob_present = await process_store(store_key, sm)
    await write_sm_blob(container_name, store_key, store_json, lease, store_blob_present)
    return store_json


async def perform_franchisee_tran(fran_key: str,
                                  loc_id: str,
                                  rest_no: str,
                                  fran_id: str,
                                  store_json: Dict):
    fran_json, lease, fran_blob_present = await process_franchisee(fran_key, loc_id, rest_no, fran_id, store_json)
    await write_sm_blob(container_name, fran_key, fran_json, lease, fran_blob_present)


async def perform_emp_franchisee_tran(fran_emp_key: str, sm: Dict):
    fran_emp_json, lease, fran_emp_blob_present = await process_emp_franchisee(fran_emp_key, sm)
    await write_sm_blob(container_name, fran_emp_key, fran_emp_json, lease, fran_emp_blob_present)


async def process_store(blob_name: str,
                        sm: Dict) -> (Dict, BlobLeaseClient, bool):
    if await blob_exists(container_name, blob_name):
        logger.info(f'Store Exists: {blob_name}')

        blob_str, lease = await read_blob(container_name, blob_name)
        store_json = json.loads(blob_str)
        updated_store_json = update_emp_rec_batch(store_json, sm)
        logger.info(f'Store Record Updated: {blob_name}')
        return updated_store_json, lease, True
    else:
        new_store_json = create_emp_container_batch(sm)
        logger.info(f'Created New Store Record: {blob_name}')
        return new_store_json, None, False


async def process_franchisee(blob_name: str,
                             store_id: str,
                             rest_no: str,
                             fran_id: str,
                             store_json: Dict) -> (Dict, BlobLeaseClient, bool):
    if await blob_exists(container_name, blob_name):
        logger.info(f'Franchisee Exists: {blob_name}')

        blob_str, lease = await read_blob(container_name, blob_name)
        fran_cont_json = json.loads(blob_str)

        updated_fran_json = proc_store_rec_batch(store_id, rest_no, fran_id, fran_cont_json, store_json)
        logger.info(f'Franchisee Updated: {blob_name}')
        return updated_fran_json, lease, True
    else:
        new_fran_json = create_fran_container_batch(store_id, rest_no, fran_id, store_json)
        logger.info(f'Created New Franchisee Record: {blob_name}')
        return new_fran_json, None, False


async def process_emp_franchisee(blob_name: str,
                                 sm: Dict) -> (Dict, BlobLeaseClient, bool):
    if await blob_exists(container_name, blob_name):
        logger.info(f'Franchisee[EMP] Exists: {blob_name}')

        blob_str, lease = await read_blob(container_name, blob_name)
        cont_json = json.loads(blob_str)

        updt_cont_json = update_emp_rec_batch(cont_json, sm)
        logger.info(f'Emp Record Updated in Franchisee[EMP]: {blob_name}')
        return updt_cont_json, lease, True
    else:
        new_cont_json = create_emp_container_batch(sm)
        logger.info(f'Created New Franchisee[EMP]: {blob_name}')
        return new_cont_json, None, False


async def process_sm_lb():
    try:
        async with get_msi_cred() as credential:
            sb_client = ServiceBusClient(sb_ns_endpoint, credential)
            async with sb_client:
                logger.debug('Inside service bus client')
                receiver = sb_client.get_queue_receiver(queue_name=lb_queue_name,
                                                        receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE)
                logger.debug('After Receiver is created....')
                async with receiver:
                    logger.debug(f'Receiver Active on {lb_queue_name}')
                    async for msg in receiver:
                        try:
                            logger.debug("Received SmartSell Event: " + str(msg))
                            sm = json.loads(str(msg))
                            if sm:
                                await process_sm_message(sm)
                            logger.debug(f'Message Processed from {lb_queue_name}....')
                        except Exception as ex:
                            logger.exception(f'Exception while processing Message: {ex!r}')

    except Exception as ex:
        logger.exception(f'Exception While Creating Queue Receiver: {ex!r}')
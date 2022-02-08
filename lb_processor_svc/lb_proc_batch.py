import asyncio
import json
import logging
import os
from typing import Dict

from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient
from azure.servicebus.exceptions import ServiceBusAuthorizationError

from commons.blob_msi_util import blob_exists, read_blob, write_sm_blob
from commons.utils import get_store_key, get_fran_key, get_store_id, get_fran_emp_key
from lb_processor_svc.helpers.fran_helper_batch import proc_store_rec_batch, create_fran_container_batch
from lb_processor_svc.helpers.store_helper_batch import update_emp_rec_batch, create_emp_container_batch

logger = logging.getLogger('smartsell')

sb_ns_endpoint = 'sb://{0}.servicebus.windows.net'.format(os.environ['sb_ns_name'])
credential = DefaultAzureCredential()
lb_queue_name = os.environ["lb_queue_name"]
container_name = os.environ["lb_container_name"]


async def process_sm_message(sm: Dict):
    store_key = get_store_key(sm[0])
    fran_key = get_fran_key(sm[0])
    store_id = get_store_id(sm[0])
    fran_emp_key = get_fran_emp_key(sm[0])

    store_json = await process_store(store_key, sm)
    fran_json, fran_emp_json = await asyncio.gather(process_franchisee(fran_key, store_id, store_json),
                                                    process_emp_franchisee(fran_emp_key, sm))
    await asyncio.gather(write_sm_blob(container_name, store_key, store_json),
                         write_sm_blob(container_name, fran_key, fran_json),
                         write_sm_blob(container_name, fran_emp_key, fran_emp_json))


async def process_store(blob_name: str,
                        sm: Dict) -> Dict:
    if await blob_exists(container_name, blob_name):
        logger.info(f'Store Exists: {blob_name}')

        blob_str = await read_blob(container_name, blob_name)
        store_json = json.loads(blob_str)
        updated_store_json = update_emp_rec_batch(store_json, sm)
        logger.info(f'Store Record Updated: {blob_name}')
        return updated_store_json
    else:
        new_store_json = create_emp_container_batch(sm)
        logger.info(f'Created New Store Record: {blob_name}')
        return new_store_json


async def process_franchisee(blob_name: str,
                             store_id: str,
                             store_json: Dict) -> Dict:
    if await blob_exists(container_name, blob_name):
        logger.info(f'Franchisee Exists: {blob_name}')

        blob_str = await read_blob(container_name, blob_name)
        fran_cont_json = json.loads(blob_str)

        updated_fran_json = proc_store_rec_batch(store_id, fran_cont_json, store_json)
        logger.info(f'Franchisee Updated: {blob_name}')
        return updated_fran_json
    else:
        new_fran_json = create_fran_container_batch(store_id, store_json)
        logger.info(f'Created New Franchisee Record: {blob_name}')
        return new_fran_json


async def process_emp_franchisee(blob_name: str,
                                 sm: Dict) -> Dict:
    if await blob_exists(container_name, blob_name):
        logger.info(f'Franchisee[EMP] Exists: {blob_name}')

        blob_str = await read_blob(container_name, blob_name)
        cont_json = json.loads(blob_str)

        updt_cont_json = update_emp_rec_batch(cont_json, sm)
        logger.info(f'Emp Record Updated in Franchisee[EMP]: {blob_name}')
        return updt_cont_json
    else:
        new_cont_json = create_emp_container_batch(sm)
        logger.info(f'Created New Franchisee[EMP]: {blob_name}')
        return new_cont_json


async def process_sm_lb():
    try:
        sb_client = ServiceBusClient(sb_ns_endpoint, credential)
        with sb_client:
            logger.debug('Inside service bus client')
            receiver = sb_client.get_queue_receiver(queue_name=lb_queue_name)
            logger.debug('After Receiver is created....')
            with receiver:
                logger.debug(f'Receiver Active on {lb_queue_name}')
                for msg in receiver:
                    logger.debug("Received SmartSell Event: " + str(msg))
                    sm = json.loads(str(msg))
                    if sm:
                        await process_sm_message(sm)
                    receiver.complete_message(msg)
                    logger.debug(f'Message Removed from {lb_queue_name}....')
    except (ClientAuthenticationError, ServiceBusAuthorizationError) as ca_error:
        logger.exception(f'Exception While Creating Queue Receiver: {ca_error!r}')

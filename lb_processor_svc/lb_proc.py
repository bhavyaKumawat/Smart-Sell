import json
import logging
import os
from typing import Dict

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient
from azure.servicebus.exceptions import ServiceBusAuthorizationError
from commons.storage_helper.blob_msi_util import blob_exists, read_blob, write_sm_blob
from commons.utils import get_store_key, get_fran_key, get_loc_id, get_fran_emp_key
from azure.core.exceptions import ClientAuthenticationError
import asyncio

from lb_processor_svc.helpers.store_helper import update_emp_rec, create_emp_container
from lb_processor_svc.helpers.fran_helper import proc_store_rec, create_fran_container

logger = logging.getLogger('smartsell')

sb_ns_endpoint = 'sb://{0}.servicebus.windows.net'.format(os.environ['sb_ns_name'])
credential = DefaultAzureCredential()
lb_queue_name = os.environ["lb_queue_name"]
container_name = os.environ["lb_container_name"]


async def process_store(sm_element_str: str):
    sm_element = json.loads(sm_element_str)
    store_key = get_store_key(sm_element)
    await perform_store_blob_ops(store_key,
                                 sm_element)


async def process_fran(sm_element: Dict,
                       store_container_json: Dict):
    fran_key = get_fran_key(sm_element)
    store_id = get_loc_id(sm_element)
    await perform_fran_blob_ops(fran_key,
                                store_id,
                                store_container_json)


async def process_fran_emp(sm_element: Dict):
    # sm_element = json.loads(sm_element_str)
    fran_emp_key = get_fran_emp_key(sm_element)
    await perform_fran_emp_blob_ops(fran_emp_key,
                                    sm_element)


async def perform_store_blob_ops(blob_name: str,
                                 sm_element: Dict):
    emp_id = sm_element['EmployeeId']
    sm_amt = sm_element['SmartSellAmount']
    sm_declined = sm_element['SmartSellDeclined']
    if await blob_exists(container_name, blob_name):
        logger.info(f'Store Exists: {blob_name}')

        blob_str = await read_blob(container_name, blob_name)
        store_json = json.loads(blob_str)

        updated_store_json = update_emp_rec(store_json, emp_id, sm_amt, sm_declined)
        await asyncio.gather(write_sm_blob(container_name, blob_name, updated_store_json),
                             process_fran(sm_element, updated_store_json),
                             process_fran_emp(sm_element))
        logger.info(f'Store Record Updated: {blob_name}')
    else:
        new_store_json = create_emp_container(emp_id, sm_amt, sm_declined)
        await asyncio.gather(write_sm_blob(container_name, blob_name, new_store_json),
                             process_fran(sm_element, new_store_json),
                             process_fran_emp(sm_element))
        logger.info(f'Created New Store Record: {blob_name}')


async def perform_fran_blob_ops(blob_name: str,
                                store_id: str,
                                store_container_json: Dict):
    if await blob_exists(container_name, blob_name):
        logger.info(f'Franchisee Exists: {blob_name}')

        blob_str = await read_blob(container_name, blob_name)
        fran_cont_json = json.loads(blob_str)

        updated_franchisee_json = proc_store_rec(store_id, fran_cont_json, store_container_json)
        await write_sm_blob(container_name, blob_name, updated_franchisee_json)
        logger.info(f'Franchisee Updated: {blob_name}')
    else:
        new_franchisee_json = create_fran_container(store_id, store_container_json)
        await write_sm_blob(container_name, blob_name, new_franchisee_json)
        logger.info(f'Created New Franchisee Record: {blob_name}')


async def perform_fran_emp_blob_ops(blob_name: str,
                                    sm_element: Dict):
    emp_id = sm_element['EmployeeId']
    sm_amt = sm_element['SmartSellAmount']
    sm_declined = sm_element['SmartSellDeclined']
    if await blob_exists(container_name, blob_name):
        logger.info(f'Franchisee[EMP] Exists: {blob_name}')

        blob_str = await read_blob(container_name, blob_name)
        cont_json = json.loads(blob_str)

        updt_cont_json = update_emp_rec(cont_json, emp_id, sm_amt, sm_declined)
        await write_sm_blob(container_name, blob_name, updt_cont_json)
        logger.info(f'Emp Record Updated in Franchisee[EMP]: {blob_name}')
    else:
        new_cont_json = create_emp_container(emp_id, sm_amt, sm_declined)
        await write_sm_blob(container_name, blob_name, new_cont_json)
        logger.info(f'Created New Franchisee[EMP]: {blob_name}')


async def process_sm_lb():
    try:
        sb_client = ServiceBusClient(sb_ns_endpoint, credential)
        with sb_client:
            logger.debug('Inside service bus client')
            receiver = sb_client.get_queue_receiver(queue_name=lb_queue_name)
            logger.debug('After Receiver is created....')
            with receiver:
                logger.info(f'Receiver Active on {lb_queue_name}')
                for msg in receiver:
                    logger.debug("Received SmartSell Event: " + str(msg))
                    await process_store(str(msg))
                    receiver.complete_message(msg)
                    logger.debug(f'Message Removed from {lb_queue_name}....')
    except (ClientAuthenticationError, ServiceBusAuthorizationError) as ca_error:
        logger.exception(f'Exception While Creating Queue Receiver: {ca_error!r}')

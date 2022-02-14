import asyncio
import json
import logging
import os
from typing import Dict

from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient
from azure.servicebus.exceptions import ServiceBusAuthorizationError

from lookup_svc.lookup_broadcast_and_errors import filter_and_broadcast, lookup_errors
from lookup_svc.process_sm_lookup import sm_lookup

from lookup_svc.helpers.generate_tillno import batch_get_tills
from lookup_svc.helpers import employee_details_helper

logger = logging.getLogger('smartsell')

sb_ns_endpoint = 'sb://{0}.servicebus.windows.net'.format(os.environ['sb_ns_name'])
credential = DefaultAzureCredential()
lookup_queue_name = os.environ["lookup_queue_name"]


async def process_sm_message(sm: Dict) -> bool:
    try:
        logger.debug(f'Processing Message for Null Values {lookup_queue_name}....')
        await sm_lookup(sm)
        return True
    except Exception as ex:
        logger.exception(f'Exception while processing Queue Message: {ex!r}')
        return False


async def process_sm_lookup():
    try:
        sb_client = ServiceBusClient(sb_ns_endpoint, credential)
        with sb_client:
            logger.debug('Inside service bus client')
            receiver = sb_client.get_queue_receiver(queue_name=lookup_queue_name)
            logger.debug('After Receiver is created....')
            with receiver:
                logger.debug(f'Receiver Active on {lookup_queue_name}')
                for msg in receiver:
                    logger.debug("Received SmartSell Ingest Event: " + str(msg))
                    sm = json.loads(str(msg))
                    if sm:
                        employee_details_helper.till_numbers = await batch_get_tills(employee_details_helper.tokens)
                        results = await asyncio.gather(*(process_sm_message(sm_element) for sm_element in sm))
                        await filter_and_broadcast(results, sm)
                        await lookup_errors(results, sm)

                    receiver.complete_message(msg)
                    logger.debug(f'Message Removed from {lookup_queue_name}....')
    except (ClientAuthenticationError, ServiceBusAuthorizationError) as ca_error:
        logger.exception(f'Exception While Creating Queue Receiver: {ca_error!r}')



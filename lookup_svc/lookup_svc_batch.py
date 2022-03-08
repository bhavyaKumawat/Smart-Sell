import asyncio
import json
import logging
import os
from typing import Dict

from azure.core.exceptions import ClientAuthenticationError
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus.exceptions import ServiceBusAuthorizationError

from lookup_svc.lookup_broadcast_and_errors import filter_and_broadcast, lookup_errors
from lookup_svc.process_sm_lookup import sm_lookup


logger = logging.getLogger('smartsell')

sb_ns_endpoint = 'sb://{0}.servicebus.windows.net'.format(os.environ['sb_ns_name'])
lookup_queue_name = os.environ["lookup_queue_name"]


async def process_sm_message(sm: Dict) -> bool:
    try:
        return await sm_lookup(sm)
    except Exception as ex:
        logger.exception(f'Exception while processing Queue Message: {ex!r}')


async def process_sm_lookup():
    try:
        async with DefaultAzureCredential() as credential:
            sb_client = ServiceBusClient(sb_ns_endpoint, credential)
            async with sb_client:
                logger.debug('Inside service bus client')
                receiver = sb_client.get_queue_receiver(queue_name=lookup_queue_name)
                logger.debug('After Receiver is created....')
                async with receiver:
                    logger.debug(f'Receiver Active on {lookup_queue_name}')
                    async for msg in receiver:
                        logger.debug("Received SmartSell Ingest Event: " + str(msg))
                        sm = json.loads(str(msg))
                        if sm:
                            results = await asyncio.gather(*(process_sm_message(sm_element) for sm_element in sm))
                            await filter_and_broadcast(results, sm)
                            await lookup_errors(results, sm)

                        await receiver.complete_message(msg)
                        logger.debug(f'Message Removed from {lookup_queue_name}....')
    except (ClientAuthenticationError, ServiceBusAuthorizationError) as ca_error:
        logger.exception(f'Exception While Creating Queue Receiver: {ca_error!r}')



import asyncio
import json
import logging
import os
from typing import Dict

from azure.servicebus import ServiceBusReceiveMode
from azure.servicebus.aio import ServiceBusClient

from commons.msi_helper.msi_util import get_msi_cred
from lookup_retro.lookup_send_messages_and_errors import lookup_send_message_to_queue
from lookup_retro.process_sm_lookup import sm_lookup

logger = logging.getLogger('smartsell')

sb_ns_endpoint = 'sb://{0}.servicebus.windows.net'.format(os.environ['sb_ns_name'])
lookup_retro_queue_name = os.environ["lookup_retro_queue_name"]


async def process_sm_message(sm: Dict) -> bool:
    try:
        return await sm_lookup(sm)
    except Exception as ex:
        logger.exception(f'Exception while processing Queue Message: {ex!r}')


async def process_sm_lookup():
    try:
        async with get_msi_cred() as credential:
            sb_client = ServiceBusClient(sb_ns_endpoint, credential)
            async with sb_client:
                logger.debug('Inside service bus client')
                receiver = sb_client.get_queue_receiver(queue_name=lookup_retro_queue_name,
                                                        receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE)
                logger.debug('After Receiver is created....')
                async with receiver:
                    logger.debug(f'Receiver Active on {lookup_retro_queue_name}')
                    async for msg in receiver:
                        try:
                            logger.debug("Received SmartSell Ingest Event: " + str(msg))
                            sm = json.loads(str(msg))
                            if sm:
                                await asyncio.gather(*(process_sm_message(sm_element) for sm_element in sm))
                                await lookup_send_message_to_queue(sm)

                            logger.debug(f'Message Processed from {lookup_retro_queue_name}....')
                        except Exception as ex:
                            logger.exception(f'Exception while processing Message: {ex!r}')

    except Exception as ex:
        logger.exception(f'Exception While Creating Queue Receiver: {ex!r}')



import json
import logging
import os
from typing import Dict

from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient

from commons.db_helper.bulk_query_helper import create_query
from commons.db_helper.conn_helper import get_cursor

logger = logging.getLogger('smartsell')

sb_ns_endpoint = 'sb://{0}.servicebus.windows.net'.format(os.environ['sb_ns_name'])
archive_queue_name = os.environ["archive_queue_name"]


async def process_sm_message(sm: Dict):
    query = await create_query(sm)
    cursor, conn = await get_cursor()
    cursor.execute(query)
    logger.debug('Inserted data into database')
    conn.commit()
    logger.debug('Committing the transaction...')


async def process_sm_archive():
    try:
        async with DefaultAzureCredential() as credential:
            sb_client = ServiceBusClient(sb_ns_endpoint, credential)
            async with sb_client:
                logger.debug('Inside service bus client')
                receiver = sb_client.get_queue_receiver(queue_name=archive_queue_name)
                logger.debug('After Receiver is created....')
                async with receiver:
                    logger.debug(f'Receiver Active on {archive_queue_name}')
                    async for msg in receiver:
                        logger.debug("Received SmartSell Event: " + str(msg))
                        sm = json.loads(str(msg))
                        if sm:
                            await process_sm_message(sm)
                        await receiver.complete_message(msg)
                        logger.debug(f'Message Removed from {archive_queue_name}....')
    except Exception as e:
        logger.exception(f'Exception While Creating Queue Receiver: {e!r}')


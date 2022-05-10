import json
import logging
import os
from typing import Dict

from azure.servicebus import ServiceBusReceiveMode
from azure.servicebus.aio import ServiceBusClient

from commons.db_helper.bulk_query_helper import create_query
from commons.db_helper.conn_helper import get_cursor
from commons.msi_helper.msi_util import get_msi_cred

logger = logging.getLogger('smartsell')

sb_ns_endpoint = 'sb://{0}.servicebus.windows.net'.format(os.environ['sb_ns_name'])
archive_queue_name = os.environ["archive_queue_name"]


async def process_sm_message(sm: Dict):
    try:
        sm_copy = []

        for sm_element in sm:
            if sm_element["TransactionId"] and sm_element["LocationId"]:
                sm_copy.append(sm_element)
            else:
                logger.debug(f"Skipping SmartSell Message: {sm_element} ")

        if sm_copy:
            query = await create_query(sm_copy)
            cursor, conn = await get_cursor()
            cursor.execute(query)
            logger.debug(f'Inserted {len(sm_copy)} messages into database')
            conn.commit()
            logger.debug('Committing the transaction...')
    except Exception as e:
        logger.exception(f'Exception While Processing SmartSell Event: {e!r}')


async def process_sm_archive():
    try:
        async with get_msi_cred() as credential:
            sb_client = ServiceBusClient(sb_ns_endpoint, credential)
            async with sb_client:
                logger.debug('Inside service bus client')
                receiver = sb_client.get_queue_receiver(queue_name=archive_queue_name,
                                                        receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE)
                logger.debug('After Receiver is created....')
                async with receiver:
                    logger.debug(f'Receiver Active on {archive_queue_name}')
                    async for msg in receiver:
                        try:
                            logger.debug("Received SmartSell Event: " + str(msg))
                            sm = json.loads(str(msg))
                            if sm:
                                await process_sm_message(sm)
                            logger.debug(f'Message Processed from {archive_queue_name}....')
                        except Exception as ex:
                            logger.exception(f'Exception while processing Message: {ex!r}')

    except Exception as e:
        logger.exception(f'Exception While Creating Queue Receiver: {e!r}')


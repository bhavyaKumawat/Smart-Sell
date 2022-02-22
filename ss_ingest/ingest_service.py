import asyncio
import json
import logging
import os
from commons.storage_helper.blob_msi_util import write_sm_blob
from commons.servicebus_helper.service_bus_utils import send_message_to_queue
from commons.utils import get_ingest_key


logger = logging.getLogger()
container_name = os.environ["sm_ingest_container"]
lookup_queue_name = os.environ["lookup_queue_name"]


async def process_ingestion(sm):

    try:
        blob_write_results = await asyncio.gather(*(perform_blob_ops(sm_element) for sm_element in sm))
        await filter_and_send_message_to_queue(blob_write_results, sm)

    except Exception as ex:
        logging.exception(f'Exception while ingestion: {ex!r}')


async def perform_blob_ops(sm_element):
    blob_name = await get_ingest_key(sm_element)
    result = await write_sm_blob(container_name, blob_name, sm_element, overwrite=False)
    return result


async def filter_and_send_message_to_queue(blob_write_results, sm):
    sm_array = []
    for index, result in enumerate(blob_write_results):
        if result:
            sm_array.append(sm[index])
    if sm_array:
        sm_msg = json.dumps(sm_array)
        logging.debug(f'Sending messages to Queue.....{blob_write_results.count(True)} of {len(blob_write_results)}')
        await send_message_to_queue(sm_msg, lookup_queue_name)

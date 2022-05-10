import asyncio
import json
import logging
import os
from datetime import datetime
from commons.storage_helper.blob_msi_util import write_sm_blob
from commons.servicebus_helper.service_bus_utils import send_message_to_queue
from commons.utils import get_ingest_key, get_dt_time_from_str

logger = logging.getLogger()
container_name = os.environ["sm_ingest_container"]
lookup_queue_name = os.environ["lookup_queue_name"]
lookup_retro_queue_name = os.environ["lookup_retro_queue_name"]


async def process_ingestion(sm):
    try:
        blob_write_results = await asyncio.gather(*(perform_blob_ops(sm_element) for sm_element in sm))
        await filter_and_send_message_to_queue(blob_write_results, sm)

    except Exception as ex:
        logging.exception(f'Exception while ingestion: {ex!r}')


async def perform_blob_ops(sm_element):
    # try:
    #     blob_name = await get_ingest_key(sm_element)
    #     result = await write_sm_blob(container_name, blob_name, sm_element, overwrite=False)
    #     return result
    # except Exception as ex:
    #     logging.exception(f'Exception while performing Blob operations: {ex!r}')
    #     return False
    return True


async def filter_and_send_message_to_queue(blob_write_results, sm):
    sm_array = []
    sm_array_retro = []
    blob_write_true_count, blob_write_true_count_restro, blob_write_total, blob_write_total_restro = 0, 0, 0, 0

    for index, result in enumerate(blob_write_results):
        if get_dt_time_from_str(sm[index]["TransactionDateTime"]).date() == datetime.today().date():
            if result:
                sm_array.append(sm[index])
                blob_write_true_count += 1
            blob_write_total += 1
        else:
            if result:
                sm_array_retro.append(sm[index])
                blob_write_true_count_restro += 1
            blob_write_total_restro += 1

    if sm_array:
        sm_msg = json.dumps(sm_array)
        logging.debug(f'Sending messages to Queue.....{blob_write_true_count} of {blob_write_total}')
        await send_message_to_queue(sm_msg, lookup_queue_name)

    if sm_array_retro:
        sm_msg = json.dumps(sm_array_retro)
        logging.debug(
            f'Sending messages to Retro Queue.....{blob_write_true_count_restro} of {blob_write_total_restro}')
        await send_message_to_queue(sm_msg, lookup_retro_queue_name)

import os
import json
import asyncio
import logging
from commons.servicebus_helper.service_bus_utils import broadcast_sm, send_message_to_queue
from commons.storage_helper.blob_msi_util import write_sm_blob
from commons.utils import get_ingest_key

logger = logging.getLogger('smartsell')
container_name = os.environ["lookup_error_container"]
archive_queue = os.environ["archive_queue_name"]
broadcast_topic = os.environ["sm_broadcast_topic"]


async def filter_and_broadcast(results, sm):
    sm_array = []
    for index, result in enumerate(results):
        if result:
            sm_array.append(sm[index])
    if sm_array:
        sm_msg = json.dumps(sm_array)
        logging.debug(f'Publishing.....{results.count(True)} of {len(results)}')
        await broadcast_sm(sm_msg, broadcast_topic)


async def lookup_errors(results, sm):
    sm_array = []
    for index, result in enumerate(results):
        if not result:
            sm_array.append(sm[index])
    logging.debug(f'Sending errors to {container_name} Container.....{results.count(False)} of {len(results)}')
    await asyncio.gather(*(write_lookup_errors(sm_element) for sm_element in sm_array))
    await send_message_to_queue(json.dumps(sm_array), archive_queue)


async def write_lookup_errors(sm_element):
    blob_name = await get_ingest_key(sm_element)
    await write_sm_blob(container_name, blob_name, sm_element, overwrite=False)

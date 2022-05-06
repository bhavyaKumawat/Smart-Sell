import os
import json
import asyncio
import logging
from commons.servicebus_helper.service_bus_utils import send_message_to_queue
from commons.storage_helper.blob_msi_util import write_sm_blob
from commons.utils import get_ingest_key

logger = logging.getLogger('smartsell')
container_name = os.environ["lookup_error_container"]
archive_retro_queue_name = os.environ["archive_retro_queue_name"]


async def lookup_send_message_to_queue(results, sm):
    sm_error_array = []
    sm_array = []
    for index, result in enumerate(results):
        if not result:
            sm_error_array.append(sm[index])
        sm_array.append(sm[index])

    logging.debug(f'Sending errors to {container_name} Container.....{results.count(False)} of {len(results)}')
    await asyncio.gather(*(write_lookup_errors(sm_element) for sm_element in sm_error_array))

    logging.debug(f'Sending messages to Archive Retro Queue.....{len(results)} of {len(results)}')
    await send_message_to_queue(json.dumps(sm_array), archive_retro_queue_name)


async def write_lookup_errors(sm_element):
    blob_name = await get_ingest_key(sm_element)
    await write_sm_blob(container_name, blob_name, sm_element, overwrite=False)

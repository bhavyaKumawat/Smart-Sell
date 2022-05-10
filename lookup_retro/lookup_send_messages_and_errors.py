import json
import logging
import os

from commons.servicebus_helper.service_bus_utils import send_message_to_queue

logger = logging.getLogger('smartsell')
container_name = os.environ["lookup_error_container"]
archive_retro_queue_name = os.environ["archive_retro_queue_name"]


async def lookup_send_message_to_queue(sm):
    logging.debug(f'Sending messages to Archive Retro Queue.....{len(sm)} of {len(sm)}')
    await send_message_to_queue(json.dumps(sm), archive_retro_queue_name)
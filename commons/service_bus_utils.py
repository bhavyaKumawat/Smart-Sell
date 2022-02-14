import os
from typing import Dict
import json
from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient
from azure.identity.aio import DefaultAzureCredential

sb_ns_endpoint = 'sb://{0}.servicebus.windows.net'.format(os.environ["sb_ns_name"])
broadcast_topic = os.environ["sm_broadcast_topic"]

credential = DefaultAzureCredential()
sb_client = ServiceBusClient(sb_ns_endpoint, credential)


async def broadcast_sm(sm_msg: str):
    async with sb_client:
        sender = sb_client.get_topic_sender(broadcast_topic)
        async with sender:
            await sender.send_messages(
                ServiceBusMessage(sm_msg))


async def send_message_to_queue(sm_msg: str, lookup_queue_name: str):
    async with sb_client:
        sender = sb_client.get_queue_sender(queue_name=lookup_queue_name)
        async with sender:
            await sender.send_messages(
                ServiceBusMessage(sm_msg))

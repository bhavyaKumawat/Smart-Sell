import os

from azure.identity.aio import DefaultAzureCredential
from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient

sb_ns_endpoint = 'sb://{0}.servicebus.windows.net'.format(os.environ["sb_ns_name"])


async def broadcast_sm(sm_msg: str, topic_name):
    async with DefaultAzureCredential() as credential:
        sb_client = ServiceBusClient(sb_ns_endpoint, credential)
        async with sb_client:
            sender = sb_client.get_topic_sender(topic_name)
            async with sender:
                await sender.send_messages(
                    ServiceBusMessage(sm_msg))


async def send_message_to_queue(sm_msg: str, queue_name: str):
    async with DefaultAzureCredential() as credential:
        sb_client = ServiceBusClient(sb_ns_endpoint, credential)
        async with sb_client:
            sender = sb_client.get_queue_sender(queue_name=queue_name)
            async with sender:
                await sender.send_messages(
                    ServiceBusMessage(sm_msg))

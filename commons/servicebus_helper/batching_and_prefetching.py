import json
from typing import List
from azure.servicebus import ServiceBusReceivedMessage


async def bifurcate_messages(messages):
    bifurcated = {}
    for msg in messages:
        key = msg["LocationId"]
        if key not in bifurcated:
            bifurcated[key] = [msg]
        else:
            bifurcated[key].append(msg)

    return list(bifurcated.values())


async def merge_messages(messages: List[ServiceBusReceivedMessage]):
    merged = []
    for msg in messages:
        merged.extend(json.loads(str(msg)))
    return merged

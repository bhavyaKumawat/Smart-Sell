import os
import logging
from typing import Dict
from azure.storage.blob.aio import BlobClient
import json
from azure.identity.aio import DefaultAzureCredential

logger = logging.getLogger('smartsell')

credential = DefaultAzureCredential()
storage_acct_name = os.environ["storage_acct_name"]
storage_url = 'https://{0}.blob.core.windows.net/'.format(storage_acct_name)


def get_blob_client(container_name: str, blob_name: str) -> BlobClient:
    blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                             credential=credential)
    return blob_client


async def blob_exists(container_name: str, blob_name: str) -> bool:
    blob_client = get_blob_client(container_name, blob_name)
    return await blob_client.exists()


async def write_sm_blob(container_name: str, blob_name: str, blob_json: Dict, overwrite: bool = True) -> bool:
    try:
        blob_client = get_blob_client(container_name, blob_name)
        sm_element_json = json.dumps(blob_json)
        await blob_client.upload_blob(sm_element_json, overwrite=overwrite)
        return True
    except Exception as ex:
        logger.exception(f'Exception while writing Blob: {ex!r}')
        return False


async def read_blob(container_name: str, blob_name: str) -> str:
    try:
        blob_client = get_blob_client(container_name, blob_name)
        blob_stream = await blob_client.download_blob()
        blob_byte_data = await blob_stream.readall()
        json_string = blob_byte_data.decode('utf-8')
        return json_string
    except Exception as ex:
        logger.exception(f'Exception while reading Blob: {ex!r}')
        return '{}'

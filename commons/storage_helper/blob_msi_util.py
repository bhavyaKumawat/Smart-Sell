import os
import logging
from typing import Dict
from azure.storage.blob.aio import BlobClient, ContainerClient
import json
from azure.identity.aio import DefaultAzureCredential

logger = logging.getLogger('smartsell')

storage_acct_name = os.environ["storage_acct_name"]
storage_url = 'https://{0}.blob.core.windows.net/'.format(storage_acct_name)


# async def get_blob_client(container_name: str, blob_name: str) -> BlobClient:
#     credential = DefaultAzureCredential()
#     blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
#                              credential=credential)
#     return blob_client


async def blob_exists(container_name: str, blob_name: str) -> bool:
    credential = DefaultAzureCredential()
    async with credential:
        blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                 credential=credential)
        return await blob_client.exists()


async def write_sm_blob(container_name: str, blob_name: str, blob_json: Dict, overwrite: bool = True) -> bool:
    try:
        credential = DefaultAzureCredential()
        async with credential:
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            sm_element_json = json.dumps(blob_json)
            await blob_client.upload_blob(sm_element_json, overwrite=overwrite)
            return True
    except Exception as ex:
        logger.exception(f'Exception while writing Blob: {ex!r}')
        return False


async def read_blob(container_name: str, blob_name: str) -> str:
    try:
        credential = DefaultAzureCredential()
        async with credential:
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            blob_stream = await blob_client.download_blob()
            blob_byte_data = await blob_stream.readall()
            json_string = blob_byte_data.decode('utf-8')
            return json_string
    except Exception as ex:
        logger.exception(f'Exception while reading Blob: {ex!r}')
        return '{}'


async def read_blob_as_bytes(container_name: str, blob_name: str):
    try:
        credential = DefaultAzureCredential()
        async with credential:
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            blob_data = await blob_client.download_blob()
            blob_byte_data = await blob_data.content_as_bytes()
            return blob_byte_data
    except Exception as ex:
        logger.exception(f'Exception while reading Blob: {ex!r}')
        return bytes()


async def delete_directory(container_name: str, dir_name: str):
    try:
        credential = DefaultAzureCredential()
        async with credential:
            container_client = ContainerClient(account_url=storage_url, container_name=container_name,
                                               credential=credential)
            blobs = container_client.list_blobs(name_starts_with=dir_name)
            await container_client.delete_blobs(*[b async for b in blobs])
    except Exception as ex:
        logger.exception(f'Exception while deleting Blobs: {ex!r}')
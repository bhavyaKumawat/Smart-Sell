import json
import logging
import os
from typing import Dict

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob.aio import BlobClient, ContainerClient, BlobLeaseClient
from fastapi import UploadFile

from commons.msi_helper.msi_util import get_msi_cred

logger = logging.getLogger('smartsell')

storage_acct_name = os.environ["storage_acct_name"]
storage_url = 'https://{0}.blob.core.windows.net/'.format(storage_acct_name)


async def blob_exists(container_name: str, blob_name: str) -> bool:
    async with get_msi_cred() as credential:
        blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                 credential=credential)
        return await blob_client.exists()


async def write_sm_blob(container_name: str, blob_name: str, blob_json: Dict,
                        lease: BlobLeaseClient, blob_present, overwrite: bool = True) -> bool:
    try:
        async with get_msi_cred() as credential:
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            sm_element_json = json.dumps(blob_json)
            if blob_present:
                await blob_client.upload_blob(sm_element_json, lease=lease, overwrite=overwrite)
                await lease.release()
            else:
                await blob_client.upload_blob(sm_element_json, overwrite=overwrite)
            return True
    except Exception as ex:
        logger.exception(f'Exception while writing Blob: {ex!r}')
        return False


async def read_blob(container_name: str, blob_name: str) -> (str, BlobLeaseClient):
    try:
        async with get_msi_cred() as credential:
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            lease = None
            while not lease:
                try:
                    lease = await blob_client.acquire_lease(lease_duration=30)
                    blob_stream = await blob_client.download_blob(lease=lease)
                    blob_byte_data = await blob_stream.readall()
                    json_string = blob_byte_data.decode('utf-8')
                    return json_string, lease

                except Exception:
                    continue

    except Exception as ex:
        logger.exception(f'Exception while reading Blob: {ex!r}')
        return '{}', None


async def read_blob_without_lease(container_name: str, blob_name: str) -> str:
    try:
        async with get_msi_cred() as credential:
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)

            while not lease:
                try:
                    lease = await blob_client.acquire_lease(lease_duration=30)
                    blob_stream = await blob_client.download_blob(lease=lease)
                    await lease.release()
                except Exception:
                    continue

            blob_byte_data = await blob_stream.readall()
            json_string = blob_byte_data.decode('utf-8')
            return json_string
    except Exception as ex:
        logger.exception(f'Exception while reading Blob: {ex!r}')
        return '{}'


async def read_blob_as_bytes(container_name: str, blob_name: str):
    try:
        async with get_msi_cred() as credential:
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            blob_data = await blob_client.download_blob()
            blob_byte_data = await blob_data.content_as_bytes()
            return blob_byte_data
    except Exception as ex:
        logger.exception(f'Exception while reading Blob: {ex!r}')
        return bytes()


async def write_file(container_name: str, blob_name: str, blob: UploadFile, overwrite: bool = True):
    async with get_msi_cred() as credential:
        blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                 credential=credential)
        await blob_client.upload_blob(blob, overwrite=overwrite)


async def read_file(container_name: str, blob_name: str):
    try:
        async with get_msi_cred() as credential:
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            blob_stream = await blob_client.download_blob()

            content_type = blob_stream.properties["content_settings"]["content_type"]
            name = blob_stream.properties["name"]
            blob_byte_data = await blob_stream.readall()
            return blob_byte_data, content_type, name
    except ResourceNotFoundError as ex:
        logger.exception(f'File does not exist: {ex!r}')
        raise


async def delete_directory(container_name: str, dir_name: str):
    try:
        async with get_msi_cred() as credential:
            container_client = ContainerClient(account_url=storage_url, container_name=container_name,
                                               credential=credential)
            blobs = container_client.list_blobs(name_starts_with=dir_name)
            await container_client.delete_blobs(*[b async for b in blobs])
    except Exception as ex:
        logger.exception(f'Exception while deleting Blob: {ex!r}')
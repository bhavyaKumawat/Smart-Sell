import logging
import os

from azure.core.exceptions import ResourceNotFoundError

from commons.storage_helper.blob_msi_util import write_file, read_file
from fastapi import UploadFile, Response

logger = logging.getLogger()
container_name = os.environ["doc_container"]


async def upload_file(file: UploadFile, path: str):
    try:
        blob_name = file.filename
        if path:
            blob_name = f"{path}/{file.filename}"
        await write_file(container_name, blob_name, file.file, overwrite=False)
    except Exception as ex:
        logging.exception(f'Exception while Uploading File {file.filename} : {ex!r}')


async def download_file(blob_name: str):
    try:
        return await read_file(container_name, blob_name)
    except ResourceNotFoundError as ex:
        logger.exception(f'Exception while Downloading File {blob_name}: {ex!r}')
        raise ResourceNotFoundError(f'Exception while Downloading File {blob_name}: {ex!r}')

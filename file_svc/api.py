import os
import asyncio
import logging
from io import BytesIO
from typing import List, Optional
from starlette.background import BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse
from fastapi import FastAPI, status, UploadFile, Query, Response
from file_svc.file_operations import upload_file, download_file

description = """
SmartSell API to upload and download files to container
"""
tags_metadata = [
    {
        "name": "SmartSell File",
        "description": "Upload Files",
    },
]
logger = logging.getLogger()
ss_file = FastAPI(
    title="SmartSell File API",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata
)


@ss_file.get('/', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


@ss_file.get('/v1/healthcheck', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


@ss_file.post('/api/upload')
async def upload_files(files: list[UploadFile], path: str = Query("", description="path separator /", )):
    await asyncio.gather(*(upload_file(file, path) for file in files))
    return {"filenames": [os.path.join(path, file.filename) for file in files]}


@ss_file.post('/api/download')
async def download_files(blob_name: str, bg_tasks: BackgroundTasks):
    try:
        file, content_type, name = await download_file(blob_name)
        name = os.path.basename(name)

        with open(name, "w+b") as f:
            f.write(file)
            bg_tasks.add_task(os.remove, name)
            return FileResponse(name, media_type=content_type, background=bg_tasks)
    except Exception as ex:
        return {"Error": f'{ex!r}'}

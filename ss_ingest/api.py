import asyncio
import logging
from typing import List, Optional
from fastapi import FastAPI, status
from models.smartsell import SmartSell
from models.status import Status
from ss_ingest.ingest_service import process_ingestion
from ss_ingest.statuslogs import process_status_logs
from models.log import StatusLog

description = """
SmartSell Ingest API to send smart sell events from POS

## Ingest

Used to send **send smart sell events from POS**.

"""
tags_metadata = [
    {
        "name": "SmartSell Ingest",
        "description": "Ingest SmartSell events",
    },
]
logger = logging.getLogger()
ss_ingest = FastAPI(
    title="SmartSell Ingest API",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata
)


@ss_ingest.get('/', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


@ss_ingest.get('/v1/healthcheck', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


@ss_ingest.post('/api/ingest', response_model=Status, tags=["SmartSell Ingest"])
def ingest_ss(sm: List[SmartSell]):
    sm_array = []
    for sm_element in sm:
        sm_array.append(sm_element.dict())

    logging.info(f'Creating a new event loop....')
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(process_ingestion(sm_array))
    finally:
        loop.close()
        logging.info(f'Closing the event loop....')

    return {"status": "success"}


@ss_ingest.post('/api/status')
async def write_status_logs(log: StatusLog):
    await process_status_logs(log.dict())
    return {"status": "success"}

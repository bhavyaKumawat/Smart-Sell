import asyncio
import logging
from fastapi import FastAPI, status
from models.leaderboard import Store
from models.smartsell import SmartSell
from utils_svc.utils_service import get_store_record, get_franchisee_record, get_franchisee_emp_record, \
    clear_all_records, insert_sm

description = """
SmartSell Utilities API to retrieve Records from Blobs

"""
tags_metadata = [
    {
        "name": "SmartSell Utilities",
        "description": "Retrieve Records from Blobs",
    },
]
logger = logging.getLogger()

ss_utils = FastAPI(
    title="SmartSell Utilities API",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata
)


@ss_utils.get('/', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


@ss_utils.get('/v1/healthcheck', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


@ss_utils.get('/api/store/{loc_id}')
async def dashboard(loc_id: str):
    return await get_store_record(loc_id)


@ss_utils.get('/api/franchisee/{fran_id}')
async def dashboard(fran_id: str):
    return await get_franchisee_record(fran_id)


@ss_utils.get('/api/franchisee-employee/{fran_id}')
async def dashboard(fran_id: str):
    return await get_franchisee_emp_record(fran_id)


@ss_utils.post('/api/clear-records')
async def dashboard():
    await clear_all_records()
    return {"status": "ok"}


@ss_utils.post('/api/insert-into-database')
async def dashboard(sm: SmartSell):
    await insert_sm(sm.dict())
    return {"status": "ok"}


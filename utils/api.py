import logging
from fastapi import FastAPI, status
from models.smartsell import SmartSell
from utils.utils_service import get_store_record, get_franchisee_record, get_franchisee_emp_record, \
    clear_all_records, insert_sm

description = """
SmartSell Utilities API to retrieve Store Records for Today.

"""
tags_metadata = [
    {
        "name": "SmartSell Utilities",
        "description": "Retrieve Store Records for Today",
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
async def get_store(loc_id: str):
    return await get_store_record(loc_id)


@ss_utils.get('/api/franchisee/store/{fran_id}')
async def get_store_in_franchisee(fran_id: str):
    return await get_franchisee_record(fran_id)


@ss_utils.get('/api/franchisee/employee/{fran_id}')
async def get_employee_in_franchisee(fran_id: str):
    return await get_franchisee_emp_record(fran_id)


@ss_utils.post('/api/clear-lb')
async def clear_blob_data():
    await clear_all_records()
    return {"status": "ok"}


@ss_utils.post('/api/archive')
async def archive(sm: SmartSell):
    await insert_sm(sm.dict())
    return {"status": "ok"}


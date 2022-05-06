import json
import logging
import os
import asyncio
from typing import Dict
from commons.utils import get_now_key
from commons.db_helper.conn_helper import get_cursor
from commons.storage_helper.blob_msi_util import blob_exists, read_blob, delete_directory
from commons.db_helper.single_query_helper import create_query
from utils_svc.helpers.utils import get_store_key, get_fran_key, get_fran_emp_key

logger = logging.getLogger()
lb_container_name = os.environ["lb_container_name"]
ingest_container_name = os.environ["sm_ingest_container"]


async def get_store_record(loc_id: str):
    loc_id = loc_id.upper()
    blob_name = get_store_key(loc_id)

    if await blob_exists(lb_container_name, blob_name):
        logger.info(f'Store Exists: {blob_name}')
        blob_str = await read_blob(lb_container_name, blob_name)
        store_json = json.loads(blob_str)
        logger.info(f'Retrieving Store Record: {blob_name}')
        return store_json
    else:
        logger.info(f'Store Record Does Not Exist: {blob_name}')
        return []


async def get_franchisee_record(fran_id: str):
    blob_name = get_fran_key(fran_id)

    if await blob_exists(lb_container_name, blob_name):
        logger.info(f'Franchisee Exists: {blob_name}')
        blob_str = await read_blob(lb_container_name, blob_name)
        fran_json = json.loads(blob_str)
        logger.info(f'Retrieving Franchisee Record: {blob_name}')
        return fran_json
    else:
        logger.info(f'Franchisee Record Does Not Exist: {blob_name}')
        return []


async def get_franchisee_emp_record(fran_id: str):
    blob_name = get_fran_emp_key(fran_id)

    if await blob_exists(lb_container_name, blob_name):
        logger.info(f'Franchisee[EMP] Exists: {blob_name}')
        blob_str = await read_blob(lb_container_name, blob_name)
        fran_json = json.loads(blob_str)
        logger.info(f'Retrieving Franchisee[EMP] Record: {blob_name}')
        return fran_json
    else:
        logger.info(f'Franchisee[EMP] Record Does Not Exist: {blob_name}')
        return []


async def clear_all_records():
    blob_name = get_now_key()
    await asyncio.gather(delete_directory(lb_container_name, blob_name),
                         delete_directory(ingest_container_name, blob_name))


async def insert_sm(sm: Dict):
    try:
        query = await create_query(sm)
        cursor, conn = await get_cursor()
        cursor.execute(query)
        logger.debug('Inserted data into database')
        conn.commit()
        logger.debug('Transaction Committed...')
    except Exception as ex:
        logger.exception(f'Exception while Inserted data into database: {ex!r}')

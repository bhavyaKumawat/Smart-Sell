from typing import Dict

from pandas import DataFrame

from commons.utils import get_fran_emp_now_key, get_fran_now_key
from lb_user_svc.helpers.utils import read_container, get_rank


async def read_fran_cont(fran_id: str, mode: str) -> DataFrame:
    blob_name = get_fran_now_key(fran_id)
    df = await read_container(blob_name, mode)
    return df


async def read_fran_emp_cont(fran_id: str, mode: str) -> DataFrame:
    blob_name = get_fran_emp_now_key(fran_id)
    df = await read_container(blob_name, mode)
    return df


def get_store_rank(store_id: str, fran_df: DataFrame) -> int:
    return get_rank(store_id, 'LocationId', fran_df)


def get_emp_network_rank(emp_id: str, network_df: DataFrame) -> int:
    return get_rank(emp_id, 'EmployeeId', network_df)


def get_top_emp_network(count: int, fran_emp_df: DataFrame) -> Dict:
    return get_top_store(count, fran_emp_df)


def get_top_store(count: int, fran_df: DataFrame) -> Dict:
    return get_top_store(count, fran_df)

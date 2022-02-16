from typing import Dict

from pandas import DataFrame

from commons.utils import get_store_now_key
from lb_user_svc.helpers.utils import find_rec_json, read_container, get_rank, get_top


async def read_store_cont(store_id: str, mode: str) -> DataFrame:
    blob_name = get_store_now_key(store_id)
    df = await read_container(blob_name, mode)
    return df


def get_emp(emp_id: str, store_df: DataFrame) -> Dict:
    return find_rec_json(emp_id, 'EmployeeId', store_df)


def get_emp_by_till(till_no: int, store_df: DataFrame) -> Dict:
    return find_rec_json(till_no, 'TillNumber', store_df)


def get_store(store_id: str, fran_df: DataFrame) -> Dict:
    return find_rec_json(store_id, 'LocationId', fran_df)


def get_emp_rank(emp_id: str, store_df: DataFrame) -> int:
    return get_rank(emp_id, 'EmployeeId', store_df)


def get_emp_rank_by_till(till_no: int, store_df: DataFrame) -> int:
    return get_rank(till_no, 'TillNumber', store_df)


def get_top_emp(count: int, store_df: DataFrame) -> Dict:
    return get_top(store_df, count)

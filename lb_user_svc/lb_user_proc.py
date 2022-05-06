import json
import asyncio
import os
import logging

from commons.storage_helper.blob_msi_util import read_blob
from lb_user_svc.helpers.fran_helper import read_fran_cont, read_fran_emp_cont, \
    get_emp_network_rank, get_store_rank, get_emp_network_rank_by_till
from lb_user_svc.helpers.response import get_response_template

from lb_user_svc.helpers.store_helper import read_store_cont, get_emp_rank, get_emp, get_store, get_emp_by_till, \
    get_emp_rank_by_till
from lb_user_svc.helpers.utils import get_top

from lb_user_svc.helpers.utils import find_rec_json
from commons.utils import is_emp_id_null

container_name = os.environ["lb_container_name"]
lookup_container_name = os.environ["sm_lookup_container"]
loc_fran_blob_name = os.environ["loc_fran_blob"]

sort_by_col = 'SuccessSmartSellCount'

logger = logging.getLogger()


async def lb_dash_start(loc_id: str, till_no: int, rank_mode: str, emp_id: str = ""):
    top_count = 10
    loc_id = loc_id.upper()

    store_df, blob_str = await asyncio.gather(read_store_cont(loc_id, rank_mode),
                                              read_blob(lookup_container_name, loc_fran_blob_name))

    fran_json = json.loads(blob_str)
    fran_id = fran_json.get(loc_id, None)

    fran_df, fran_emp_df = await asyncio.gather(read_fran_cont(fran_id, rank_mode),
                                                read_fran_emp_cont(fran_id, rank_mode))

    response_json = get_response_template()

    if not store_df.empty:
        emp = get_emp_by_till(till_no, store_df) if is_emp_id_null(emp_id) else get_emp(emp_id, store_df)

        if bool(emp):
            response_json["employee"] = emp[0]
            emp_in_st_rank = get_emp_rank_by_till(till_no, store_df) if is_emp_id_null(emp_id) else get_emp_rank(emp_id,
                                                                                                                 store_df)
            emp_in_net_rank = get_emp_network_rank_by_till(till_no, store_df) if is_emp_id_null(
                emp_id) else get_emp_network_rank(emp_id, fran_emp_df)
            response_json["employee"]["rank"] = {
                "restaurant": emp_in_st_rank,
                "network": emp_in_net_rank
            }
        else:
            response_json["employee"]["EmployeeId"] = emp_id
        top_emp = get_top(store_df, top_count)
        response_json["top_emp_in_store"] = top_emp

    if not fran_df.empty:
        store = get_store(loc_id, fran_df)
        st_in_fran_rank = get_store_rank(loc_id, fran_df)
        response_json["store"] = store[0]
        response_json["store"]["rank"] = {
            "network": st_in_fran_rank
        }
        top_st = get_top(fran_df, top_count)
        response_json["top_store_in_network"] = top_st

    if not fran_emp_df.empty:
        top_emp_network = get_top(fran_emp_df, top_count)
        response_json["top_emp_in_network"] = top_emp_network

    logger.debug(f'Response JSON {response_json}')
    return response_json


async def get_store_details(store_id, fran_id, rank_mode):
    fran_df = await read_fran_cont(fran_id, rank_mode)
    if not fran_df.empty:
        store = get_store(store_id, fran_df)
        if bool(store):
            st_in_fran_rank = get_store_rank(store_id, fran_df)
            response_json = store[0]
            response_json["rank"] = {
                "network": st_in_fran_rank
            }
            top_st = get_top(fran_df)
            response_json["top_store_in_network"] = top_st
            return response_json
    return {}

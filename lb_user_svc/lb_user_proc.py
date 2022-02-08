import asyncio
import os

from lb_user_svc.helpers.fran_helper import read_fran_cont, read_fran_emp_cont, \
    get_emp_network_rank, get_store_rank
from lb_user_svc.helpers.response import get_response_template
import pprint

from lb_user_svc.helpers.store_helper import read_store_cont, get_emp_rank, get_emp, get_store
from lb_user_svc.helpers.utils import get_top

container_name = os.environ["lb_container_name"]
sort_by_col = 'SuccessSmartSellCount'


async def lb_dash_start(emp_id: str, store_id: str, fran_id: str, rank_mode: str):
    top_count = 10
    store_df, fran_df, fran_emp_df = await asyncio.gather(read_store_cont(store_id, rank_mode),
                                                          read_fran_cont(fran_id, rank_mode),
                                                          read_fran_emp_cont(fran_id, rank_mode))
    response_json = get_response_template()

    if not store_df.empty:
        emp = get_emp(emp_id, store_df)
        if bool(emp):
            print(type(emp[0]['SuccessSmartSellCount']))
            response_json["employee"] = emp[0]
            emp_in_st_rank = get_emp_rank(emp_id, store_df)
            emp_in_net_rank = get_emp_network_rank(emp_id, fran_emp_df)
            response_json["employee"]["rank"] = {
                "restaurant": emp_in_st_rank,
                "network": emp_in_net_rank
            }
        else:
            response_json["employee"]["EmployeeId"] = emp_id
        top_emp = get_top(store_df, top_count)
        response_json["top_emp_in_store"] = top_emp

    if not fran_df.empty:
        store = get_store(store_id, fran_df)
        st_in_fran_rank = get_store_rank(store_id, fran_df)
        response_json["store"] = store[0]
        response_json["store"]["rank"] = {
            "network": st_in_fran_rank
        }
        top_st = get_top(fran_df, top_count)
        response_json["top_store_in_network"] = top_st

    if not fran_df.empty:
        top_emp_network = get_top(fran_emp_df, top_count)
        response_json["top_emp_in_network"] = top_emp_network

    # res_str = json.dumps(response_json)
    pprint.pprint(response_json)
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
            pprint.pprint(response_json)
            return response_json
    return {}

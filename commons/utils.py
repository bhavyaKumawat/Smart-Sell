from datetime import datetime
import logging
import asyncio
from typing import Dict

logger = logging.getLogger('smartsell')


async def get_ingest_key(sm_element: Dict):
    try:
        return '{0}/{1}/{2}/{3}_{4}.json'.format(get_dt_key(sm_element['TransactionDateTime']), sm_element['LocationId'],
                                                 sm_element['TerminalId'], str(sm_element['Id']),
                                                 sm_element['TransactionId'])
    except Exception as ex:
        raise


def get_emp_key(sm_element: Dict):
    return '{0}/{1}/{2}.json'.format(get_dt_key(sm_element['TransactionDateTime']), sm_element['LocationId'],
                                     sm_element['EmployeeId'])


def get_store_key(sm_element: Dict):
    return '{0}/{1}.json'.format(get_dt_key(sm_element['TransactionDateTime']), sm_element['LocationId'])


def get_loc_id(sm_element: Dict):
    return sm_element['LocationId'].upper()


def get_fran_key(sm_element: Dict):
    fran_id = sm_element['FranchiseeId'] if sm_element.get("FranchiseeId") else 'arbys'
    return '{0}/{1}.json'.format(get_dt_key(sm_element['TransactionDateTime']), fran_id)


def get_fran_emp_key(sm_element: Dict):
    fran_id = sm_element['FranchiseeId'] if sm_element.get("FranchiseeId") else 'arbys'
    return '{0}/{1}.json'.format(get_dt_key(sm_element['TransactionDateTime']), fran_id + '-emp')


def get_dt_key(transaction_date_time):
    try:
        date_format_str = "%m/%d/%Y %H:%M:%S %p"
        date_obj = datetime.strptime(transaction_date_time, date_format_str)
        sm_date_str = date_obj.strftime('%m-%d-%Y')
        return sm_date_str
    except Exception as ex:
        raise


def get_store_now_key(store_id: str):
    return '{0}/{1}.json'.format(get_now_key(), store_id)


def get_fran_now_key(fran_id: str) -> str:
    fran_id = fran_id
    return '{0}/{1}.json'.format(get_now_key(), fran_id)


def get_fran_emp_now_key(fran_id: str) -> str:
    fran_id = fran_id + '-emp'
    return '{0}/{1}.json'.format(get_now_key(), fran_id)


def get_now_key():
    now = datetime.now()
    sm_date_str = now.strftime('%m-%d-%Y')
    return sm_date_str


def till_number_exists(sm_element: Dict) -> bool:
    if sm_element['TillNumber'] != 0:
        return True
    else:
        return False


def get_dt_time_from_str(transaction_date_time: str):
    date_format_str = "%m/%d/%Y %H:%M:%S %p"
    date_obj = datetime.strptime(transaction_date_time, date_format_str)
    return date_obj


def get_now_date_time():
    now = datetime.now()
    sm_date_str = now.strftime('%m/%d/%Y %H:%M:%S %p')
    return sm_date_str


def get_sm_tran_date(transaction_date_time: str):
    date_obj = get_dt_time_from_str(transaction_date_time)
    sm_date_str = date_obj.strftime('%Y-%m-%d')
    return sm_date_str


def is_emp_id_null(emp_id):
    if emp_id == "" or emp_id == "0":
        return True
    else:
        return False

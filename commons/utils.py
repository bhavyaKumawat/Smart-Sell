from datetime import datetime
import logging
from typing import Dict

logger = logging.getLogger('smartsell')


def get_ingest_key(sm_element: Dict):
    return '{0}/{1}/{2}/{3}_{4}.json'.format(get_dt_key(sm_element['TransactionDateTime']), sm_element['LocationId'],
                                             sm_element['TerminalId'], sm_element['Id'], sm_element['TransactionId'])


def get_emp_key(sm_element: Dict):
    return '{0}/{1}/{2}.json'.format(get_dt_key(sm_element['TransactionDateTime']), sm_element['LocationId'],
                                     sm_element['EmployeeId'])


def get_store_key(sm_element: Dict):
    return '{0}/{1}.json'.format(get_dt_key(sm_element['TransactionDateTime']), sm_element['LocationId'])


def get_store_id(sm_element: Dict):
    return sm_element['LocationId']


def get_fran_key(sm_element: Dict):
    return '{0}/{1}.json'.format(get_dt_key(sm_element['TransactionDateTime']), 'arbys')


def get_fran_emp_key(sm_element: Dict):
    return '{0}/{1}.json'.format(get_dt_key(sm_element['TransactionDateTime']), 'arbys-emp')


def get_dt_key(transaction_date_time):
    date_format_str = "%m/%d/%Y %H:%M:%S %p"
    date_obj = datetime.strptime(transaction_date_time, date_format_str)
    sm_date_str = date_obj.strftime('%m-%d-%Y')
    return sm_date_str


def get_store_now_key(store_id: str):
    return '{0}/{1}.json'.format(get_now_key(), store_id)


def get_fran_now_key(fran_id: str) -> str:
    fran_id = 'arbys'
    return '{0}/{1}.json'.format(get_now_key(), fran_id)


def get_fran_emp_now_key(fran_id: str) -> str:
    fran_id = 'arbys' + '-emp'
    return '{0}/{1}.json'.format(get_now_key(), fran_id)


def get_now_key():
    now = datetime.now()
    sm_date_str = now.strftime('%m-%d-%Y')
    return sm_date_str

import logging
from commons.utils import get_now_key

logger = logging.getLogger()


def get_store_key(loc_id: str):
    return '{0}/{1}.json'.format(get_now_key(), loc_id)


def get_fran_key(fran_id: str):
    return '{0}/{1}.json'.format(get_now_key(), fran_id)


def get_fran_emp_key(fran_id: str):
    return '{0}/{1}.json'.format(get_now_key(), fran_id + '-emp')

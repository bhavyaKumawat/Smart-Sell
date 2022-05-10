import logging
import os
from typing import Dict

from commons.emp_details_helper.area_supervisor_helper import get_area_supervisor
from commons.emp_details_helper.employee_details_helper import get_employee_details
from commons.emp_details_helper.rest_number_helper import get_rest_number
from commons.utils import is_emp_id_null, get_sm_tran_date, is_till_number_null

logger = logging.getLogger('smartsell')
container_name = os.environ["sm_lookup_container"]


async def sm_lookup(sm: Dict) -> bool:
    try:

        sm['LocationId'] = sm['LocationId'].upper()

        emp_lookup_result = await emp_id_lookup(sm)
        store_lookup_result = await store_lookup(sm)

        if emp_lookup_result and store_lookup_result:
            return True
        else:
            return False

    except Exception as ex:
        logger.exception(f'Exception while processing Queue Message: {ex!r}')
        return False


async def emp_id_lookup(sm):
    try:
        if is_emp_id_null(sm["EmployeeId"]):
            logger.info(f'Looking up for EmployeeId with TillNumber: {sm["TillNumber"]} and LocationId: {sm["LocationId"]}')

            if is_till_number_null(sm["TillNumber"]):
                logger.info(f'Lookup failed due to Till Number: {sm["TillNumber"]}')
                return False

            emp_details = await get_employee_details(sm["TillNumber"],
                                                     sm['LocationId'],
                                                     get_sm_tran_date(sm['TransactionDateTime']))
            if emp_details == {}:
                return False
            sm['EmployeeId'] = emp_details['EmployeeId']
            logger.info(f'EmployeeId Lookup Successful. EmployeeId: {sm["EmployeeId"]}')
        else:
            logger.info(f'Skipping Looking up for EmployeeId as it is found as {sm["EmployeeId"]}')
        return True
    except Exception as ex:
        logger.exception(f'Exception while Emp ID lookup: {ex!r}')
        return False


async def store_lookup(sm):
    try:
        logger.info(f'Looking up for Rest Number with LocationId: {sm["LocationId"]}')
        rest_no = await get_rest_number(sm['LocationId'])
        if rest_no == "":
            logger.info(f"Rest Number lookup failed for location_id: {sm['LocationId']}")
            return False
        logger.info(f'Rest Number Lookup Successful. Rest Number: {rest_no}')
        logger.info(f'Looking up for franchisee_id with Rest Number: {rest_no}')
        franchisee_id = await get_area_supervisor(rest_no)
        if franchisee_id == "":
            logger.info(f'franchisee_id lookup failed for rest_no:{rest_no}')
            return False

        sm['FranchiseeId'], sm['Rest_Number'] = franchisee_id, rest_no
        logger.info(f'franchisee_id Lookup Successful. FranchiseeId: {sm["FranchiseeId"]}')

        return True
    except Exception as ex:
        logger.exception(f'Exception while Store ID lookup: {ex!r}')
        return False


import logging
from typing import Dict

from lookup_svc.helpers.employee_details_helper import get_employee_details
from commons.functional_helper.rest_number_helper import get_rest_number
from commons.functional_helper.area_supervisor_helper import get_area_supervisor

logger = logging.getLogger('smartsell')


async def sm_lookup(sm: Dict) -> Dict:
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
        if sm["EmployeeId"] == "":
            emp_details = await get_employee_details(sm["TillNumber"])
            if emp_details['EmployeeId'] == "":
                return False
            sm['EmployeeId'] = emp_details['EmployeeId']

        return True
    except Exception as ex:
        logger.exception(f'Exception while Emp ID lookup: {ex!r}')
        return False


async def store_lookup(sm):
    try:

        rest_no = await get_rest_number(sm['LocationId'])
        if rest_no == "":
            return False
        franchisee_id = await get_area_supervisor(rest_no)
        if franchisee_id == "":
            return False
        sm['FranchiseeId'], sm['Rest_Number'] = franchisee_id, rest_no
        return True
    except Exception as ex:
        logger.exception(f'Exception while Store ID lookup: {ex!r}')
        return False


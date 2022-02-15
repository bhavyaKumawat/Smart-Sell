import logging
from typing import Dict

from lookup_svc.helpers.employee_details_helper import get_employee_details
from commons.functional_helper.rest_number_helper import get_rest_number
from commons.functional_helper.area_supervisor_helper import get_area_supervisor


logger = logging.getLogger('smartsell')


async def sm_lookup(sm: Dict) -> Dict:
    try:
        if sm["EmployeeId"] == "":
            emp_details = await get_employee_details(sm["TillNumber"])
            sm['EmployeeId'] = emp_details['EmployeeId']
        rest_no = await get_rest_number(sm['LocationId'])
        franchisee_id = await get_area_supervisor(rest_no)

        sm['FranchiseeId'], sm['Rest_Number'] = franchisee_id, rest_no
        return sm
    except Exception as ex:
        logger.exception(f'Exception while processing Queue Message: {ex!r}')
        return sm





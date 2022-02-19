import os
import asyncio
import logging
from typing import Dict

from commons.emp_details_helper import rest_number_helper
from commons.emp_details_helper.generate_tillno import get_tills

logger = logging.getLogger()


async def get_employee_details(till_no: int, loc_id: str) -> Dict:
    try:
        dictionary = rest_number_helper.dictionary
        location_code = dictionary[loc_id]["LocationCode"]
        access_token = os.environ["AccessToken"]

        till_numbers = await get_tills(location_code, access_token)
        return till_numbers[till_no]

    except Exception as ex:
        logger.exception(f'Exception while getting Employee Details: {ex!r}')
        return {}

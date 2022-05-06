import logging

from commons.emp_details_helper.area_supervisor_helper import get_area_supervisor
from commons.emp_details_helper.rest_number_helper import get_rest_number

logger = logging.getLogger('smartsell')


async def get_fran_id(location_id: str) -> str:
    try:
        logger.info(f'Looking up for Rest Number with LocationId: {location_id}')
        rest_no = await get_rest_number(location_id)
        if rest_no == "":
            logger.info(f'Rest Number lookup failed')
            return ""
        logger.info(f'Rest Number Lookup Successful. Rest Number: {rest_no}')
        logger.info(f'Looking up for franchisee_id with Rest Number: {rest_no}')
        franchisee_id = await get_area_supervisor(rest_no)
        if franchisee_id == "":
            logger.info(f'franchisee_id lookup failed')
            return ""

        logger.info(f'franchisee_id Lookup Successful. FranchiseeId: {franchisee_id}')

        return franchisee_id
    except Exception as ex:
        logger.exception(f'Exception while franchisee ID lookup: {ex!r}')
        return ""

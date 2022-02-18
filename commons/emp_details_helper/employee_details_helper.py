import os
import asyncio
import logging
from typing import Dict

from commons.emp_details_helper.file_helper import create_lookup_dictionary
from commons.emp_details_helper.generate_tillno import batch_get_tills

logger = logging.getLogger()

container_name = os.environ["sm_lookup_container"]
blob_name = os.environ["arbys_tokens_blob"]
sheet_name = os.environ["arbys_tokens_sheet"]

tokens = asyncio.run(create_lookup_dictionary(container_name,
                                              blob_name,
                                              index_col='LocationId',
                                              sheet_name=sheet_name,
                                              usecols=("LocationId", "LocationToken", "AccessToken"),
                                              orient="dict"))

till_numbers = asyncio.run(batch_get_tills(tokens))


async def get_employee_details(till_no: int) -> Dict:
    try:
        global till_numbers
        return till_numbers[till_no]

    except Exception as ex:
        logger.exception(f'Exception while getting Employee Details: {ex!r}')

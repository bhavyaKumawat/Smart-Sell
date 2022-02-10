import os
import asyncio
import logging

from lookup_svc.helpers.read_blob_helper import create_lookup_dictionary

logger = logging.getLogger()
container_name = os.environ["sm_lookup_container"]
blob_name = os.environ["store_data_blob"]


dictionary = asyncio.run(create_lookup_dictionary(container_name,
                                                  blob_name,
                                                  index_col='REST_NUMBER',
                                                  sheet_name="Sheet1",
                                                  usecols=("REST_NUMBER", "REST_L2NAME")))


async def get_area_supervisor(rest_number: int) -> str:
    global dictionary
    try:
        return dictionary[rest_number]
    except Exception as ex:
        logger.exception(f'Exception while getting Restaurant Number: {ex!r}')


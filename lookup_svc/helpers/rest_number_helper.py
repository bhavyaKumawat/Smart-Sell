import os
import asyncio
import logging

from lookup_svc.helpers.read_blob_helper import create_lookup_dictionary

logger = logging.getLogger()
container_name = os.environ["sm_lookup_container"]
blob_name = os.environ["loc_restno_blob"]


dictionary = asyncio.run(create_lookup_dictionary(container_name,
                                                  blob_name,
                                                  index_col='LocationID',
                                                  sheet_name="Location_Codes",
                                                  skiprows=1,
                                                  usecols=("Number", "LocationID")))


async def get_rest_number(location_id: str) -> int:
    global dictionary
    try:
        return int(dictionary[location_id][4:])
    except Exception as ex:
        logger.exception(f'Exception while getting Restaurant Number: {ex!r}')

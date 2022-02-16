import os
import asyncio
import logging

from lookup_svc.helpers.file_helper import create_lookup_dictionary

logger = logging.getLogger()
container_name = os.environ["sm_lookup_container"]
blob_name = os.environ["loc_restno_blob"]
sheet_name = os.environ["loc_restno_sheet"]


dictionary = asyncio.run(create_lookup_dictionary(container_name,
                                                  blob_name,
                                                  index_col='LocationID',
                                                  sheet_name=sheet_name,
                                                  skiprows=1,
                                                  usecols=("Number", "LocationID")))


async def get_rest_number(location_id: str) -> int:
    try:
        global dictionary
        loc_id = dictionary.get(location_id.lower()) if dictionary.get(location_id.lower()) else dictionary.get(location_id.upper())
        return int(loc_id[4:])
    except Exception as ex:
        logger.exception(f'Exception while getting Restaurant Number: {ex!r}')

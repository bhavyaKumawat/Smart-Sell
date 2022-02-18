import logging
import pandas as pd
from commons.storage_helper.blob_msi_util import read_blob_as_bytes

logger = logging.getLogger()


async def create_lookup_dictionary(container_name: str, blob_name: str, index_col: str, sheet_name: str = None,
                                   skiprows: int = 0, usecols: tuple = None, orient: str = 'records') -> dict:
    try:
        blob_byte_data = await read_blob_as_bytes(container_name, blob_name)
        dataframe = pd.read_excel(blob_byte_data,
                                  sheet_name=sheet_name,
                                  usecols=usecols,
                                  skiprows=skiprows).dropna(axis=0, how='any')

        dictionary = dataframe.set_index(index_col).T.to_dict(orient)
        logger.debug(f'Creating lookup Dictionary for {blob_name}....')

        return dictionary[0] if orient == 'records' else dictionary
    except Exception as ex:
        logger.exception(f'Exception while creating lookup Dictionary: {ex!r}')
        return {}



import logging
import pandas as pd
from commons.blob_msi_util import get_blob_client

logger = logging.getLogger()


async def read_blob_as_bytes(container_name: str, blob_name: str):
    try:
        blob_client = get_blob_client(container_name, blob_name)
        blob_data = await blob_client.download_blob()
        blob_byte_data = await blob_data.content_as_bytes()
        return blob_byte_data
    except Exception as ex:
        logger.exception(f'Exception while reading Blob: {ex!r}')
        return bytes()


async def create_lookup_dictionary(container_name: str, blob_name: str, index_col: str, sheet_name: str = None,
                                   skiprows: int = 0, usecols: tuple = None) -> dict:
    try:
        blob_byte_data = await read_blob_as_bytes(container_name, blob_name)
        dataframe = pd.read_excel(blob_byte_data,
                                  sheet_name=sheet_name,
                                  usecols=usecols,
                                  skiprows=skiprows).dropna(axis=0, how='any')
        dictionary = dataframe.set_index(index_col).T.to_dict('records')[0]
        return dictionary
    except Exception as ex:
        logger.exception(f'Exception while creating Restaurant Number lookup Dictionary: {ex!r}')
        return {}

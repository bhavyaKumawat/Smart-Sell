import json
import os
from typing import Dict

import pandas as pd
from pandas import DataFrame

from commons.storage_helper.blob_msi_util import read_blob

# sort_by_col = 'SmartSellAmount'
container_name = os.environ["lb_container_name"]


def get_top(df: DataFrame, count: int = 10) -> Dict:
    top_def = df.head(count)
    return json.loads(top_def.to_json(orient='records'))


async def read_container(blob_name: str, mode: str = "Volume") -> DataFrame:
    blob_str = await read_blob(container_name, blob_name)
    cont_json = json.loads(blob_str)
    cont_df = pd.DataFrame(cont_json)
    sort_by_col = get_sort_col_name(mode)
    return sort_df(sort_by_col, cont_df)


def sort_df(col: str, df: DataFrame) -> DataFrame:
    if df.empty:
        return df
    df.sort_values(by=[col], inplace=True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    return df


def get_rank(key_id, col: str, df: DataFrame) -> int:
    rec = df.loc[df[col] == key_id]
    if (not rec.empty) and (rec.loc[rec.index[0]]["SuccessSmartSellCount"]):
        return int(rec.index[0]) + 1
    else:
        return 0


def get_top_by(count: int, col: str, df: DataFrame) -> Dict:
    top_def = df.top(count)
    return json.loads(top_def.to_json(orient='records'))


def find_rec_json(key_id: str, col: str, df: DataFrame) -> Dict:
    rec = df.loc[df[col] == key_id]
    return json.loads(rec.to_json(orient='records'))


def get_sort_col_name(mode: str = "Volume"):
    if mode == 'Volume':
        return 'SmartSellAmount'
    else:
        return 'Percentage'

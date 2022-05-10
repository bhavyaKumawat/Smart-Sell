import json
from typing import Dict
import pandas as pd
from pandas import DataFrame


def proc_store_rec(store_id: str, fran_json: Dict,
                   store_cont_json: Dict) -> Dict:
    franchisee_df = pd.DataFrame(fran_json)
    store_rec_json = evaluate_store_rec(store_id, pd.DataFrame(store_cont_json))
    store_exists = store_id in franchisee_df.values
    if store_exists:
        store_rec = franchisee_df.loc[franchisee_df['LocationId'] == store_id]
        franchisee_df.at[store_rec.index[0], 'SmartSellAmount'] = store_rec_json['SmartSellAmount']
        franchisee_df.at[store_rec.index[0], 'SuccessSmartSellCount'] = store_rec_json['SuccessSmartSellCount']
        franchisee_df.at[store_rec.index[0], 'TotalSmartSellCount'] = store_rec_json['TotalSmartSellCount']
    else:
        franchisee_df = franchisee_df.append(store_rec_json, ignore_index=True)
    return json.loads(franchisee_df.to_json(orient='records'))


def create_fran_container(store_id: str, store_container_json: Dict):
    # col_names = ['LocationId', 'SmartSellAmount', 'SuccessSmartSellCount', 'TotalSmartSellCount']
    # df = pd.DataFrame(columns=col_names)
    new_store_json = evaluate_store_rec(store_id, pd.DataFrame(store_container_json))
    # df.append(, ignore_index=True)
    df = pd.DataFrame([new_store_json])
    return json.loads(df.to_json(orient='records'))


def evaluate_store_rec(store_id: str, store_cont_df: DataFrame) -> Dict:
    return \
        {
            "LocationId": store_id,
            "SmartSellAmount": store_cont_df['SmartSellAmount'].sum(),
            "SuccessSmartSellCount": store_cont_df['SuccessSmartSellCount'].sum(),
            "TotalSmartSellCount": store_cont_df['TotalSmartSellCount'].sum()
        }

import json
from typing import Dict
import pandas as pd
from pandas import DataFrame


def proc_store_rec_batch(store_id: str, rest_no: str, fran_id: str, fran_json: Dict,
                         store_cont_json: Dict) -> Dict:
    franchisee_df = pd.DataFrame(fran_json)
    store_rec_json = evaluate_store_rec(store_id, rest_no, fran_id, pd.DataFrame(store_cont_json))
    store_exists = store_id in franchisee_df.values
    if store_exists:
        store_rec = franchisee_df.loc[franchisee_df['LocationId'] == store_id]
        franchisee_df.at[store_rec.index[0], 'SmartSellAmount'] = store_rec_json['SmartSellAmount']
        franchisee_df.at[store_rec.index[0], 'SuccessSmartSellCount'] = store_rec_json['SuccessSmartSellCount']
        franchisee_df.at[store_rec.index[0], 'TotalSmartSellCount'] = store_rec_json['TotalSmartSellCount']
        franchisee_df.at[store_rec.index[0], 'Percentage'] = round(store_rec_json['Percentage'], 2)
        franchisee_df.at[store_rec.index[0], 'FranchiseeId'] = store_rec_json['FranchiseeId']
    else:
        franchisee_df = franchisee_df.append(store_rec_json, ignore_index=True)
    return json.loads(franchisee_df.to_json(orient='records'))


def create_fran_container_batch(store_id: str, rest_no: str, fran_id: str, store_container_json: Dict):
    new_store_json = evaluate_store_rec(store_id, rest_no, fran_id, pd.DataFrame(store_container_json))
    df = pd.DataFrame([new_store_json])
    return json.loads(df.to_json(orient='records'))


def evaluate_store_rec(store_id: str, rest_no: str, fran_id: str, store_cont_df: DataFrame) -> Dict:
    amount = store_cont_df['SmartSellAmount'].sum()
    count = store_cont_df['SuccessSmartSellCount'].sum()
    total_count = store_cont_df['TotalSmartSellCount'].sum()
    percentage = (store_cont_df['SuccessSmartSellCount'].sum() / store_cont_df['TotalSmartSellCount'].sum()) * 100
    percentage = round(percentage, 2)
    return \
        {
            "LocationId": store_id,
            "Rest_Number": rest_no,
            "SmartSellAmount": amount,
            "SuccessSmartSellCount": count,
            "TotalSmartSellCount": total_count,
            "Percentage": percentage,
            "FranchiseeId": fran_id
        }

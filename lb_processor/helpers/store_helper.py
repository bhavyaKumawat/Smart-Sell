import json
from typing import Dict
import pandas as pd


def update_emp_rec(store_json: Dict,
                   emp_id: str,
                   sm_amt: float,
                   sm_declined: int) -> Dict:
    store_df = pd.DataFrame(store_json)
    emp_exists = emp_id in store_df.values
    if emp_exists:
        emp_rec = store_df.loc[store_df['EmployeeId'] == emp_id]
        orig_amount = emp_rec.at[emp_rec.index[0], 'SmartSellAmount']
        orig_count = emp_rec.at[emp_rec.index[0], 'SuccessSmartSellCount']
        orig_total = emp_rec.at[emp_rec.index[0], 'TotalSmartSellCount']
        if sm_declined == 0:
            store_df.at[emp_rec.index[0], 'SmartSellAmount'] = orig_amount + sm_amt
            store_df.at[emp_rec.index[0], 'SuccessSmartSellCount'] = orig_count + 1
            store_df.at[emp_rec.index[0], 'Percentage'] = (orig_count + 1)/(orig_total+1) * 100
        else:
            store_df.at[emp_rec.index[0], 'Percentage'] = orig_count / (orig_total + 1) * 100
        store_df.at[emp_rec.index[0], 'TotalSmartSellCount'] = orig_total + 1
    else:
        new_emp_rec = create_new_emp_json(emp_id, sm_amt, sm_declined)
        store_df = store_df.append(new_emp_rec, ignore_index=True)

    return json.loads(store_df.to_json(orient='records'))


def create_emp_container(emp_id: str,
                         sm_amt: float,
                         sm_declined: int):
    new_emp_json = create_new_emp_json(emp_id, sm_amt, sm_declined)
    df = pd.DataFrame([new_emp_json])
    return json.loads(df.to_json(orient='records'))


def create_new_emp_json(emp_id: str,
                        sm_amt: float,
                        sm_declined: int):
    if sm_declined == 0:
        return \
            {
                'EmployeeId': emp_id,
                'SmartSellAmount': sm_amt,
                'SuccessSmartSellCount': 1,
                'TotalSmartSellCount': 1,
                'Percentage': 100
            }
    else:
        return \
            {
                'EmployeeId': emp_id,
                'SmartSellAmount': 0,
                'SuccessSmartSellCount': 0,
                'TotalSmartSellCount': 1,
                'Percentage': 0
            }

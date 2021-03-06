import json
from typing import Dict
import pandas as pd
import logging

from commons.utils import till_number_exists

logger = logging.getLogger('smartsell')


def update_emp_rec_batch(store_json: Dict, sm: Dict) -> Dict:
    store_df = pd.DataFrame(store_json)
    for sm_element in sm:
        if till_number_exists(sm_element):
            emp_id = sm_element['EmployeeId']
            sm_amt = sm_element['SmartSellAmount']
            sm_declined = sm_element['SmartSellDeclined']
            emp_name = sm_element['EmployeeName']
            till_no: int = sm_element['TillNumber']
            fran_id = sm_element['FranchiseeId']

            emp_exists = emp_id in store_df.values
            if emp_exists:
                emp_rec = store_df.loc[store_df['EmployeeId'] == emp_id]
                orig_amount = emp_rec.at[emp_rec.index[0], 'SmartSellAmount']
                orig_count = emp_rec.at[emp_rec.index[0], 'SuccessSmartSellCount']
                orig_total = emp_rec.at[emp_rec.index[0], 'TotalSmartSellCount']
                orig_count, orig_total = float(orig_count), float(orig_total)

                emp_name = emp_name if (emp_rec.at[emp_rec.index[0], 'EmployeeName']) == "" else emp_rec.at[
                    emp_rec.index[0], 'EmployeeName']

                if sm_declined == 0:
                    store_df.at[emp_rec.index[0], 'SmartSellAmount'] = orig_amount + sm_amt
                    store_df.at[emp_rec.index[0], 'SuccessSmartSellCount'] = orig_count + 1
                    store_df.at[emp_rec.index[0], 'Percentage'] = round(((orig_count + 1) / (orig_total + 1) * 100), 2)
                else:
                    store_df.at[emp_rec.index[0], 'Percentage'] = round((orig_count / (orig_total + 1) * 100), 2)
                store_df.at[emp_rec.index[0], 'TotalSmartSellCount'] = orig_total + 1
                store_df.at[emp_rec.index[0], 'TillNumber'] = till_no
                store_df.at[emp_rec.index[0], 'EmployeeName'] = emp_name

            else:
                new_emp_rec = create_new_emp_json(emp_id, emp_name, till_no, fran_id, sm_amt, sm_declined)
                store_df = store_df.append(new_emp_rec, ignore_index=True)
        else:
            logger.info("TillNumber missing, ignoring the smart sell..")
    return json.loads(store_df.to_json(orient='records'))


def create_emp_container_batch(sm: Dict):
    column_names = ['EmployeeId', 'EmployeeName', 'SmartSellAmount', 'SuccessSmartSellCount', 'TotalSmartSellCount',
                    'Percentage', 'FranchiseeId', 'TillNumber']
    store_df = pd.DataFrame(columns=column_names)
    for sm_element in sm:
        if till_number_exists(sm_element):
            emp_id = sm_element['EmployeeId']
            sm_amt = sm_element['SmartSellAmount']
            sm_declined = sm_element['SmartSellDeclined']
            emp_name = sm_element['EmployeeName']
            till_no: int = sm_element['TillNumber']
            fran_id = sm_element['FranchiseeId']

            emp_exists = emp_id in store_df.values
            if emp_exists:
                emp_rec = store_df.loc[store_df['EmployeeId'] == emp_id]
                orig_amount = emp_rec.at[emp_rec.index[0], 'SmartSellAmount']
                orig_count = emp_rec.at[emp_rec.index[0], 'SuccessSmartSellCount']
                orig_total = emp_rec.at[emp_rec.index[0], 'TotalSmartSellCount']
                orig_count, orig_total = float(orig_count), float(orig_total)

                if sm_declined == 0:
                    store_df.at[emp_rec.index[0], 'SmartSellAmount'] = orig_amount + sm_amt
                    store_df.at[emp_rec.index[0], 'SuccessSmartSellCount'] = orig_count + 1
                    store_df.at[emp_rec.index[0], 'Percentage'] = round(((orig_count + 1) / (orig_total + 1) * 100), 2)
                else:
                    store_df.at[emp_rec.index[0], 'Percentage'] = round((orig_count / (orig_total + 1) * 100), 2)
                store_df.at[emp_rec.index[0], 'TotalSmartSellCount'] = orig_total + 1
                store_df.at[emp_rec.index[0], 'TillNumber'] = till_no
            else:
                new_emp_rec = create_new_emp_json(emp_id, emp_name, till_no, fran_id, sm_amt, sm_declined)
                store_df = store_df.append(new_emp_rec, ignore_index=True)
    store_df['TillNumber'] = store_df['TillNumber'].astype(int)
    return json.loads(store_df.to_json(orient='records'))


def create_new_emp_json(emp_id: str,
                        emp_name: str,
                        till_no: int,
                        fran_id: str,
                        sm_amt: float,
                        sm_declined: int):
    if sm_declined == 0:
        return \
            {
                'EmployeeId': emp_id,
                'EmployeeName': emp_name,
                'TillNumber': till_no,
                'FranchiseeId': fran_id,
                'SmartSellAmount': sm_amt,
                'SuccessSmartSellCount': 1,
                'TotalSmartSellCount': 1,
                'Percentage': 100.0
            }
    else:
        return \
            {
                'EmployeeId': emp_id,
                'EmployeeName': emp_name,
                'TillNumber': till_no,
                'FranchiseeId': fran_id,
                'SmartSellAmount': 0.0,
                'SuccessSmartSellCount': 0,
                'TotalSmartSellCount': 1,
                'Percentage': 0.0
            }

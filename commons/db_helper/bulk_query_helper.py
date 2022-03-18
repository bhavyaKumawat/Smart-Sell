from typing import Dict

from commons.utils import get_dt_time_from_str, get_now_date_time


async def create_query(sm: Dict) -> str:
    query = """INSERT INTO SmartSellLogs (
                TransactionId, 
                CreatedBy,
                CreatedOn,
                OrderId,
                SmartSellItemId,
                SmartSellGroupId,
                SmartSellLinkedItemId,
                SmartSellDeclined,
                SmartSellAmount,
                RuleID,
                CrewSmartSellTimeInMs,
                EmployeeId,
                EmployeeName,
                TerminalId,
                TerminalName,
                LocationId,
                StoreId, 
                TransactionDateTime)
            VALUES
            """

    for sm_element in sm:
        query += f"""( '{sm_element["TransactionId"]}' ,
                    '{sm_element["EmployeeId"]}',
                    '{get_now_date_time()}',
                    '{sm_element["OrderId"]}',
                    '{sm_element["SmartSellItemId"]}',
                    '{sm_element["SmartSellGroupId"]}',
                    '{sm_element["SmartSellLinkedItemId"]}',
                    {sm_element["SmartSellDeclined"]},
                    {sm_element["SmartSellAmount"]},
                    {sm_element["RuleId"]},
                    {sm_element["CrewSmartSellTimeInMs"]},
                    '{sm_element["EmployeeId"]}',
                    '{sm_element["EmployeeName"]}',
                    '{sm_element["TerminalId"]}',
                    '{sm_element["TerminalName"]}',
                    '{sm_element["LocationId"]}',
                    '{sm_element["Rest_Number"]}',
                    '{get_dt_time_from_str(sm_element["TransactionDateTime"])}' ),"""

    return query[:-1] + ";"

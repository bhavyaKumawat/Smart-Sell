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

    query += f"""( '{sm["TransactionId"]}' ,
                '{sm["EmployeeId"]}',
                '{get_now_date_time()}',
                '{sm["OrderId"]}',
                '{sm["SmartSellItemId"]}',
                '{sm["SmartSellGroupId"]}',
                '{sm["SmartSellLinkedItemId"]}',
                {sm["SmartSellDeclined"]},
                {sm["SmartSellAmount"]},
                {sm["RuleId"]},
                {sm["CrewSmartSellTimeInMs"]},
                '{sm["EmployeeId"]}',
                '{sm["EmployeeName"]}',
                '{sm["TerminalId"]}',
                '{sm["TerminalName"]}',
                '{sm["LocationId"]}',
                '{sm["Rest_Number"]}',
                '{get_dt_time_from_str(sm["TransactionDateTime"])}' );"""

    return query

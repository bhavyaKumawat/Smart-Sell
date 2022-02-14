from typing import Dict
from commons.utils import get_dt_key, get_loc_id, get_now_key


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
                TransactionDateTime,
                RowCreatedOn)
            VALUES
            """

    for sm_element in sm:
        query += f"""( NEWID() ,
                    '{"default"}',
                    '{get_now_key()}',
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
                    NEWID(),
                    '{get_loc_id(sm_element)}',
                    '{get_dt_key(sm_element["TransactionDateTime"])}',
                    '{get_now_key()}' ),"""

    return query[:-1] + ";"

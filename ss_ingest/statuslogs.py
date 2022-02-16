import logging
import asyncio
from typing import Dict
from commons.utils import get_dt_time_from_str
from commons.functional_helper.conn_helper import get_cursor
from commons.functional_helper.rest_number_helper import get_rest_number

logger = logging.getLogger()


async def process_status_logs(sm, blob_write_results):
    try:
        logger.debug('Writing logs to SmartSellStatusLogs...')
        await asyncio.gather(*(write_log(sm[index], status) for index, status in enumerate(blob_write_results)))
    except Exception as ex:
        logging.exception(f'Exception while Writing logs to SmartSellStatusLogs : {ex!r}')


async def write_log(sm: Dict, status: bool):
    query = await create_logs_query(sm, status)
    cursor, conn = await get_cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


async def create_logs_query(sm: Dict, status: bool) -> str:

    rest_number = await get_rest_number(sm['LocationId']) if sm["Rest_Number"] == "" else sm["Rest_Number"]

    query = """INSERT INTO SmartSellStatusLogs (
                CreatedBy, 
                SmartSellStatus,
                TransactionDateTime,
                LocationId,
                TerminalId,
                TerminalName,
                StoreId)
            VALUES
            """

    query += f"""( '{sm["EmployeeId"]}' ,
                 {int(status)},
                '{get_dt_time_from_str(sm["TransactionDateTime"])}',
                '{sm["LocationId"]}',
                '{sm["TerminalId"]}',
                '{sm["TerminalName"]}',
                '{rest_number}'),"""

    return query[:-1] + ";"

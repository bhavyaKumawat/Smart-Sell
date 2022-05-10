import logging
from commons.utils import get_dt_time_from_str
from commons.db_helper.conn_helper import get_cursor
from commons.emp_details_helper.rest_number_helper import get_rest_number

logger = logging.getLogger()


async def process_status_logs(log):
    try:
        await write_log(log)
    except Exception as ex:
        logging.exception(f'Exception while Writing logs to SmartSellStatusLogs : {ex!r}')


async def write_log(log):
    query = await create_logs_query(log)
    cursor, conn = await get_cursor()
    logger.debug('Writing logs to SmartSellStatusLogs...')
    cursor.execute(query)
    conn.commit()
    conn.close()
    logger.debug('Committing the transaction...')


async def create_logs_query(log) -> str:
    try:
        rest_number = await get_rest_number(log["LocationId"])

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

        query += f"""( '{log["CreatedBy"]}' ,
                     {int(log["SmartSellStatus"])},
                    '{get_dt_time_from_str(log["TransactionDateTime"])}',
                    '{log["LocationId"]}',
                    '{log["TerminalId"]}',
                    '{log["TerminalName"]}',
                    '{rest_number}'),"""

        return query[:-1] + ";"
    except Exception as ex:
        logging.exception(f'Exception while Creating Query : {ex!r}')

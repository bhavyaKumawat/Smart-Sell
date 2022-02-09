import asyncio
import logging

from fastapi import FastAPI, status


description = """
SmartSell Archive Processor API to INSERT smart sell events INTO SQL Server. 

## Archive Processor

Used to INSERT smart sell events INTO SQL Server.

"""

logger = logging.getLogger()

archive_processor = FastAPI(
    title="Archive Processor API",
    description=description,
    version="0.0.1"
)


@archive_processor.get('/', status_code=status.HTTP_200_OK)
def heath_check():
    logger.info('Health Check')
    print(__name__)
    return {"status": "ok"}


@archive_processor.get('/v1/healthcheck', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


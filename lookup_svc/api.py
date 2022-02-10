import asyncio
import logging
from fastapi import FastAPI, status


description = """
## Lookup Service

SmartSell Lookup Service API to lookup Employee-Id, Employee-Name, Rest-Number and Area-Supervisor.

"""

logger = logging.getLogger()

lookup_service = FastAPI(
    title="Lookup Service API",
    description=description,
    version="0.0.1"
)


@lookup_service.get('/', status_code=status.HTTP_200_OK)
def heath_check():
    logger.info('Health Check')
    print(__name__)
    return {"status": "ok"}


@lookup_service.get('/v1/healthcheck', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


import asyncio
import logging

from fastapi import FastAPI, status

from lb_processor_svc.lb_proc_batch import process_sm_lb

description = """
SmartSell LeaderBoard Processor API to process smart sell events. 🚀

## LeaderBoard Processor

Used to process SmartSell Events and Prepare Leaderboard data.

"""

logger = logging.getLogger()

lb_processor = FastAPI(
    title="LeaderBoard API",
    description=description,
    version="0.0.1"
)


@lb_processor.get('/', status_code=status.HTTP_200_OK)
def heath_check():
    logger.info('Health Check')
    print(__name__)
    return {"status": "ok"}


@lb_processor.get('/v1/healthcheck', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


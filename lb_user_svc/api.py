import logging

from fastapi import FastAPI, HTTPException, status

from lb_user_svc.lb_user_proc import lb_dash_start, get_store_details
from models.leaderboard import LeaderBoard, Store
from models.rank_mode import RankMode

description = """
SmartSell LeaderBoard API to view employee's performance. 🚀

## LeaderBoard

Used to  query for **Employees Performance for SmartSell**.

## Get Store

Used to get the **Store/Restaurant Details**
"""
tags_metadata = [
    {
        "name": "LeaderBoard",
        "description": "View the LeaderBoard Dashboard for a employee",
    },
    {
        "name": "Store",
        "description": "View the specific Store Details"
    },
]
logger = logging.getLogger()

leaderboard = FastAPI(
    title="LeaderBoard API",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata
)


@leaderboard.get('/', status_code=status.HTTP_200_OK)
def heath_check():
    logger.info('Health Check')
    print(__name__)
    return {"status": "ok"}


@leaderboard.get('/v1/healthcheck', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


@leaderboard.get('/api/leaderboard/{emp_id}/{store_id}/{fran_id}/{rank_mode}', response_model=LeaderBoard,
                 tags=["LeaderBoard"])
async def dashboard(emp_id: str, store_id: str, fran_id: str, rank_mode: RankMode):
    return await lb_dash_start(emp_id, store_id, fran_id, rank_mode.value)


@leaderboard.get('/api/store/{store_id}/{fran_id}/{rank_mode}', response_model=Store, tags=["Store"])
async def get_store(store_id: str, fran_id: str, rank_mode: RankMode):
    store_details = await get_store_details(store_id, fran_id, rank_mode.value)
    if bool(store_details):
        return store_details
    else:
        raise HTTPException(status_code=404, detail="Store not found")

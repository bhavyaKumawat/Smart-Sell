import logging
from typing import Optional

from fastapi import FastAPI, HTTPException, status

from lb_user_svc.lb_user_proc import lb_dash_start, get_store_details
from models.leaderboard import LeaderBoard, Store
from models.rank_mode import RankMode
from fastapi.middleware.cors import CORSMiddleware

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

leaderboard.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@leaderboard.get('/', status_code=status.HTTP_200_OK)
def heath_check():
    logger.info('Health Check')
    print(__name__)
    return {"status": "ok"}


@leaderboard.get('/v1/healthcheck', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


@leaderboard.get('/api/leaderboard/{loc_id}/{till_no}/{rank_mode}', response_model=LeaderBoard,
                 tags=["LeaderBoard"])
async def dashboard(loc_id: str, till_no: int, rank_mode: RankMode, emp_id: Optional[str] = ""):
    return await lb_dash_start(loc_id, till_no, rank_mode.value, emp_id)

from typing import Optional

from pydantic import BaseModel


class StatusLog(BaseModel):
    CreatedBy: str
    SmartSellStatus: bool
    TransactionDateTime: str
    LocationId: str
    TerminalId: str
    TerminalName: Optional[str]

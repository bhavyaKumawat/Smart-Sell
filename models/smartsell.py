from pydantic import BaseModel
from typing import Optional


class SmartSell(BaseModel):
    Id: int
    TransactionId: str
    OrderId: str
    SmartSellItemId: Optional[str]
    SmartSellLinkedItemId: str
    SmartSellDeclined: int
    SmartSellAmount: float
    SmartSellGroupId: Optional[int]
    RuleId: int
    TransactionDateTime: str
    TerminalId: int
    TerminalName: str
    LocationId: str
    IsSent: int
    EmployeeName: Optional[str]
    EmployeeId: Optional[str]
    Rest_Number: Optional[str]
    CrewSmartSellTimeInMs: int
    TillNumber: int

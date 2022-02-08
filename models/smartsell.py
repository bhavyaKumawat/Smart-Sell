from pydantic import BaseModel


class SmartSell(BaseModel):
    Id: str
    TransactionId: str
    OrderId: str
    SmartSellItemId: str
    SmartSellLinkedItemId: str
    SmartSellDeclined: int
    SmartSellAmount: float
    SmartSellGroupId: int
    RuleId: int
    TransactionDateTime: str
    TerminalId: int
    TerminalName: str
    LocationId: str
    IsSent: int
    EmployeeName: str
    EmployeeId: str
    Rest_Number: str
    CrewSmartSellTimeInMs: int

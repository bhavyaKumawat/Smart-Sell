from typing import Optional, List

from pydantic import BaseModel


class Rank(BaseModel):
    restaurant: Optional[int] = 0
    network: Optional[int] = 0


class Store(BaseModel):
    LocationId: Optional[str]
    Rest_Number: Optional[str]
    SmartSellAmount: float
    SuccessSmartSellCount: int
    TotalSmartSellCount: int
    Percentage: Optional[float] = 0.0
    rank: Optional[Rank]


class Employee(BaseModel):
    EmployeeId: Optional[str]
    EmployeeName: Optional[str]
    Rest_Number: Optional[str]
    SmartSellAmount: float
    SuccessSmartSellCount: int
    TotalSmartSellCount: int
    Percentage: Optional[float] = 0.0
    rank: Optional[Rank] = None


class LeaderBoard(BaseModel):
    employee: Employee
    store: Store
    top_emp_in_store: Optional[List[Employee]]
    top_emp_in_network: Optional[List[Employee]]
    top_store_in_network: Optional[List[Store]]


from pydantic import BaseModel
from typing import List



class SignalSchema(BaseModel):
    symbol: str
    side: str
    price: float
    time: str
    message: str

    class Config:
        orm_mode = True


class OrderSchema(SignalSchema):
    size: float
    leverage: int
    
    class Config:
        orm_mode = True
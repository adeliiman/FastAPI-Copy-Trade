from pydantic import BaseModel
from typing import List


class AdminSchema(BaseModel):
    percent: float
    leverage: int
    
    class Config:
        orm_mode = True

from sqlalchemy import Column, Integer, String, Float
from database import Base

class SignalModel(Base):
    __tablename__ = "signals"

    id = Column(Integer,primary_key=True,index=True)
    symbol = Column(String)
    side = Column(String)
    price = Column(Float)
    time = Column(String)
    message = Column(String)


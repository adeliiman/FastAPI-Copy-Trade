from sqlalchemy import Column,Integer, Float
from database import Base

class AdminModel(Base):
    __tablename__ = "settings"

    id = Column(Integer,primary_key=True,index=True)
    percent = Column(Float)
    leverage = Column(Integer)


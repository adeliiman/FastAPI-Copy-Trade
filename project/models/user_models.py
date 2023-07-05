
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base



class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    api_key = Column(String)
    secret_key = Column(String)


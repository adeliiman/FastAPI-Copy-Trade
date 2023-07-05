from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends





SQLALCHEMY_DATABASE_URL = "sqlite:///./copytrade.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://iman:@postgresserver/db"

engine = create_engine(url=SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_superuser():
    db = SessionLocal()
    from models.user_models import UserModel
    from utils.security import get_hash_password
    admin = db.query(UserModel).filter(UserModel.username=='admin').first()
    if not admin:
        admin = UserModel(username='admin', 
                          hashed_password=get_hash_password('admin'), 
                          is_superuser=True, 
                          is_active=True)
        db.add(admin)
        db.commit()
        db.refresh(admin)


def init_db():
    Base.metadata.create_all(bind=engine)
    create_superuser()
    

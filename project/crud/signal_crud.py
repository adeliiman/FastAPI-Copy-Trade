from sqlalchemy.orm import Session
from models.signal_models import SignalModel
from models.admin_models import AdminModel
from schemas.signal_schemas import SignalSchema
from models.user_models import UserModel
from celery_app.tasks import create_task


def add_signal(db: Session, signal: SignalSchema):
    db_signal = SignalModel(symbol=signal.symbol, 
                            side=signal.side,
                            price=signal.price,
                            time=signal.time, 
                            message=signal.message)
    db.add(db_signal)
    db.commit()
    db.refresh(db_signal)
    return db_signal


def get_signals(db: Session, skip: int=0, limit: int=10):
    return db.query(SignalModel).offset(skip).limit(limit).all()


def get_signals_by_symbol(symbol: str, db: Session, skip: int=0, limit: int=10):
    return db.query(SignalModel).where(SignalModel.symbol==symbol).offset(skip).limit(limit).all()


def get_signals_by_side(side: str, db: Session, skip: int=0, limit: int=10):
    return db.query(SignalModel).where(SignalModel.side==side).offset(skip).limit(limit).all()


def trade(signal: SignalSchema, db: Session):
    setting = db.query(AdminModel).first()
    leverage = setting.leverage
    percent = setting.percent
    db_users = db.query(UserModel).all()
    for user in db_users:
        if user.is_active:
            try:
                print('run ...')
                create_task.apply_async((user.api_key, user.secret_key, leverage, percent, signal))
            except Exception as e:
                print(e)
   
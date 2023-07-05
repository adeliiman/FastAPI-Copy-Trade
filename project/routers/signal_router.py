from typing import List
from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from crud import signal_crud
from database import get_db
from schemas.signal_schemas import SignalSchema


router = APIRouter(tags=['signal'])


@router.post("/webhook", response_model=SignalSchema, summary="Add New Signal")
async def add_signal(signal: SignalSchema, 
                     db: Session = Depends(get_db)):
    signal_crud.trade(signal.dict(), db)
    return signal_crud.add_signal(db=db, signal=signal)


@router.get("/latest", response_model=List[SignalSchema], summary="Get Latest Signals")
def get_signals( skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return signal_crud.get_signals(db, skip=skip, limit=limit)


@router.get("/symbol/", response_model=List[SignalSchema], summary="Get Signals by Symbol")
def get_signals_by_symbol(symbol: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return signal_crud.get_signals_by_symbol(db=db, skip=skip, limit=limit, symbol=symbol)


@router.get("/side/", response_model=List[SignalSchema], summary="Get Signals by Side")
def get_signals_by_side(side: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return signal_crud.get_signals_by_side(db=db, skip=skip, limit=limit, side=side)



from binance_api import new_position
from celery_app.celery import app



@app.task(name="create_task")
def create_task(api_key: str, secret_key: str, leverage: int, percent: float, signal: dict):
    new_position(api_key=api_key, secret_key=secret_key, leverage=leverage, percent=percent, signal=signal)



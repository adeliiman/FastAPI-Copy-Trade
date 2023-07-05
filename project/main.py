from fastapi import FastAPI
from database import init_db
from fastapi.middleware.cors import CORSMiddleware
from routers.signal_router import router as signal_router
from routers.user_router import router as user_router
from routers.admin_router import router as admin_router
from utils.config import setting


app = FastAPI()
# app = FastAPI(openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    init_db()
    print("done")


app.router.prefix = setting.api_prefix

app.include_router(signal_router, prefix="/signal")
app.include_router(user_router, prefix="/user")
app.include_router(admin_router, prefix="/admin")

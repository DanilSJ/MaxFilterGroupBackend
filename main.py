from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from api_v1.user.views import router as user_router
from api_v1.group.views import router as group_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(user_router, tags=["user"], prefix="/user")
app.include_router(group_router, tags=["group"], prefix="/group")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7777)
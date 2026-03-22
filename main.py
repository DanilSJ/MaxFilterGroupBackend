from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from api_v1.user.views import router as user_router
from api_v1.group.views import router as group_router
from api_v1.grid.views import router as grid_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, tags=["user"], prefix="/user")
app.include_router(group_router, tags=["group"], prefix="/group")
app.include_router(grid_router, tags=["grid"], prefix="/grid")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7777)
from fastapi import FastAPI
from .core import database
from .api import authentication , register
from .model import user_mod #its very important to import these models inside main.py file to add them to database

from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core import database
from .api import authentication, register

# 1. LifeSpan Management
# This replaces the old way of creating tables. 
# It runs once when the server starts and cleans up when it stops.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with database.engine.begin() as conn:
        # This is the async way to run create_all
        await conn.run_sync(database.Base.metadata.create_all)
    
    yield
    # Shutdown: Close database connections
    await database.engine.dispose()

# 2. Initialize FastAPI with Lifespan
app = FastAPI(
    title="VaxTrace AI",
    lifespan=lifespan
)

# 3. Include Routers
app.include_router(authentication.router)
app.include_router(register.router)

@app.get("/")
async def root():
    return {"message": "Welcome to VaxTrace AI API (Async Mode)"}
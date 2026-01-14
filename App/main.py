from fastapi import FastAPI
from .core import database
from .api import authentication , register
#its very important to import these models inside main.py file to add them to database
from .model import  user_mod, vax_auditlog,vax_master,vax_schedule,patient_mod,pat_vax_plan  #its very important to import these models inside main.py file to add them to database

from .services.seed import seed_vaccine_data
from sqlalchemy.orm import Session
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core import database
from .api import authentication, register , patient , vaxplan

from fastapi.middleware.cors import CORSMiddleware

# 1. LifeSpan Management
# This replaces the old way of creating tables. 
# It runs once when the server starts and cleans up when it stops.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with database.engine.begin() as conn:
        # This is the async way to run create_all
        await conn.run_sync(database.Base.metadata.create_all)


    # 2. Run the seed function
        # We define a small wrapper to use a Session inside run_sync
         
        def do_seed(sync_conn):
            with Session(sync_conn) as session:
                seed_vaccine_data(session)
                session.commit()

        await conn.run_sync(do_seed)

        
    yield
    # Shutdown: Close database connections
    await database.engine.dispose()

# 2. Initialize FastAPI with Lifespan
app = FastAPI(
    title="VaxTrace AI",
    lifespan=lifespan
)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://localhost:5173"
              # React dev server
        
    ],
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, PUT, PATCH, DELETE
    allow_headers=["*"],   # Authorization, Content-Type, etc
)

# 3. Include Routers
app.include_router(authentication.router)
app.include_router(register.router)
app.include_router(patient.router)
app.include_router(vaxplan.router)

@app.get("/")
async def root():
    return {"message": "Welcome to VaxTrace AI API (Async Mode)"}
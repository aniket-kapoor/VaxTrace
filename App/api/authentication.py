from fastapi import APIRouter , Depends ,HTTPException , status
from fastapi.security import OAuth2PasswordRequestForm
from ..core import database
from ..schemas import user
from ..security import hashing

from ..security import token
from ..model import user_mod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.concurrency import run_in_threadpool # Best practice for hashing

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=user.TokenResponse)
async def login(
    request: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(database.get_db)
):
    # 1. Async query using select()
    query = select(user_mod.Users).where(user_mod.Users.email == request.username)
    result = await db.execute(query)
    found_user = result.scalar_one_or_none()

    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # 2. Hashing is CPU-bound. 
    # run_in_threadpool keeps the event loop free while the CPU calculates the hash.
    is_password_correct = await run_in_threadpool(
        hashing.hash.verify_password, 
        request.password, 
        found_user.hashed_password
    )
    
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Wrong Password',
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # 3. Generate token (usually synchronous unless it involves DB I/O)
    access_token = token.create_access_token(data={"sub": found_user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}
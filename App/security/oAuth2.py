from fastapi import Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from .token import verify_token

from ..model import user_mod
from ..core import database

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: AsyncSession = Depends(database.get_db) # 1. Use AsyncSession
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token, credentials_exception)

    # 2. Use 'select' and 'await db.execute'
    query = select(user_mod.Users).where(user_mod.Users.email == token_data.email)
    result = await db.execute(query)
    
    # 3. Extract the first result
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is not active"
        )
    
    return user
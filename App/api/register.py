from fastapi import APIRouter ,Depends,HTTPException,status
from ..schemas import user
from ..security import hashing

from ..services import dependency
from ..core import database
from ..model import user_mod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.concurrency import run_in_threadpool
# Import your models and schemas...

router = APIRouter(tags=['User'])

@router.post("/register", response_model=user.UserRead)
async def create_user(request: user.UserCreate, db: AsyncSession = Depends(database.get_db)):
    # Hashing is CPU-bound, offload it to a threadpool
    hashed_pwd = await run_in_threadpool(hashing.hash.get_hash_password, request.password)
    
    new_user = user_mod.Users(
        name=request.name, 
        email=request.email, 
        hashed_password=hashed_pwd, 
        role=request.role
    )
    
    db.add(new_user)
    await db.commit()      # MUST await commit
    await db.refresh(new_user)  # MUST await refresh to get the ID
    return new_user


@router.get("/get/user/{user_id}", response_model=user.UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    # Async style selection
    query = select(user_mod.Users).where(user_mod.Users.id == user_id)
    result = await db.execute(query)
    found_user = result.scalar_one_or_none()

    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) 
    
    return found_user


@router.post("/users/deactivate")
async def deactivate_account(
    request: user.DeactivateConfirmation,
    db: AsyncSession = Depends(database.get_db),
    current_user = Depends(dependency.allow_worker)
):
    if not request.confirm:
        raise HTTPException(
            status_code=400,
            detail="Confirmation required to deactivate the account"
        )
    
    current_user.is_active = False
    
    # In AsyncSession, changes to objects are tracked. 
    # Just merge/add and commit.
    db.add(current_user) 
    await db.commit()

    return {"detail": "Your account has been deactivated successfully"}

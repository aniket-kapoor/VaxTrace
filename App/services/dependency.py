from fastapi import HTTPException, Depends, status
from ..security import oAuth2

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    # Change to async def
    async def __call__(self, user = Depends(oAuth2.get_current_user)):
        # Since get_current_user is async, FastAPI awaits it before passing 'user' here
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="You don't have permission to perform this action"
            )
        return user

# Define access groups (These remain the same)
allow_admin = RoleChecker(["admin"])
allow_worker = RoleChecker(["admin", "worker"])
allow_all = RoleChecker(["admin", "worker", "parent"])
allow_parent = RoleChecker(["parent", "admin"])
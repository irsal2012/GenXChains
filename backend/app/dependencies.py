from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.utils.security import decode_token

# auto_error=False so a *missing* Authorization header surfaces as 401 (not
# FastAPI's default 403). Clients distinguish "authenticate" from "forbidden"
# by status code — the SPA clears its token and redirects to /login on 401 only.
security = HTTPBearer(auto_error=False)


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise _unauthorized("Not authenticated")
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise _unauthorized("Invalid or expired token")
    try:
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise _unauthorized("Invalid or expired token")
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise _unauthorized("User not found")
    return user


def require_roles(allowed_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}",
            )
        return current_user
    return role_checker


# Convenience role dependencies
def admin_only(user: User = Depends(require_roles(["admin"]))):
    return user


def executive_or_admin(user: User = Depends(require_roles(["admin", "executive"]))):
    return user


def planner_or_above(user: User = Depends(require_roles(["admin", "executive", "demand_planner", "supply_planner", "inventory_manager", "finance_analyst", "sop_coordinator"]))):
    return user

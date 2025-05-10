from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from api.db.session import get_db
from api.models.user import User
from api.models.role import Role  # assuming Role model exists in models/role.py
from api.schemas.user import UserSchema

router = APIRouter()

@router.get("/users", response_model=List[UserSchema], status_code=status.HTTP_200_OK)
def get_users(role: str = Query("all", description="Role filter: seller, buyer, or all"), db: Session = Depends(get_db)):
    """
    Fetch users filtered by role.
    - If role is 'seller', returns users with role 'Seller'.
    - If role is 'buyer', returns users with role 'Buyer'.
    - If role is 'all', returns all users.
    """
    query = db.query(User)
    role_filter = role.lower()
    if role_filter in ["seller", "buyer"]:
        # join Role table to filter by role_name (case-insensitive)
        # query = "select * from users u join roles r on u.role_id = r.id where r.role_name = :role_name"
        query = query.join(Role).filter(Role.role_name.ilike(role_filter))
    elif role_filter != "all":
        raise HTTPException(status_code=400, detail="Invalid role filter value. Use 'seller', 'buyer', or 'all'.")
    
    users = query.all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found for the given filter.")
    return users

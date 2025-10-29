from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db_session
from ..models.user import User
from ..schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserSchema])
async def get_users(session: AsyncSession = Depends(get_db_session)):
    """Get all users"""
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get a user by ID"""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=UserSchema)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_db_session)):
    """Create a new user"""
    new_user = User(
        username=user_data.username,
        age=user_data.age,
        eye_color=user_data.eye_color
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user_data: UserUpdate, session: AsyncSession = Depends(get_db_session)):
    """Update a user"""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only provided fields
    if user_data.username is not None:
        user.username = user_data.username
    if user_data.age is not None:
        user.age = user_data.age
    if user_data.eye_color is not None:
        user.eye_color = user_data.eye_color
    
    await session.commit()
    await session.refresh(user)
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db_session)):
    """Delete a user"""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await session.delete(user)
    await session.commit()
    return {"message": "User deleted successfully"}


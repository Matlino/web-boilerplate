"""Helper functions for Airflow tasks"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models.user import User
from .models.statistics import UserStatistics
from .db import Base
from .settings import settings


async def get_user_statistics() -> Dict[str, Any]:
    """Calculate user statistics from the database"""
    # Create async engine and session
    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    async_session_maker = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        # Total users
        total_result = await session.execute(select(func.count(User.id)))
        total_users = total_result.scalar_one()
        
        # Average age
        avg_age_result = await session.execute(select(func.avg(User.age)))
        avg_age = avg_age_result.scalar_one()
        avg_age = round(float(avg_age), 2) if avg_age else 0
        
        # Eye color distribution
        eye_color_result = await session.execute(
            select(User.eye_color, func.count(User.id))
            .group_by(User.eye_color)
        )
        eye_color_dist = {color: count for color, count in eye_color_result.all()}
        
        # Users added in last 24 hours (if we had created_at, for now we'll skip this)
        # For now, we'll just return what we have
        
        # Age distribution (min, max)
        age_stats_result = await session.execute(
            select(func.min(User.age), func.max(User.age))
        )
        min_age, max_age = age_stats_result.one()

        # Ensure tables exist in case API app isn't running
        async with session.bind.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Persist statistics
        stats_row = UserStatistics(
            calculated_at=datetime.utcnow(),
            total_users=int(total_users or 0),
            average_age=float(avg_age or 0),
            min_age=int(min_age or 0),
            max_age=int(max_age or 0),
            eye_color_distribution=eye_color_dist,
        )
        session.add(stats_row)
        await session.commit()
        
    await engine.dispose()
    
    return {
        "total_users": total_users,
        "average_age": avg_age,
        "min_age": min_age if min_age else 0,
        "max_age": max_age if max_age else 0,
        "eye_color_distribution": eye_color_dist,
        "calculated_at": datetime.utcnow().isoformat(),
    }


def run_user_statistics_sync() -> Dict[str, Any]:
    """Synchronous wrapper for Airflow task"""
    return asyncio.run(get_user_statistics())


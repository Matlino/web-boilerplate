from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db_session
from ..models.statistics import UserStatistics
from ..schemas.statistics import UserStatisticsOut


router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/latest", response_model=UserStatisticsOut)
async def get_latest_stats(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(
        select(UserStatistics).order_by(desc(UserStatistics.calculated_at)).limit(1)
    )
    stats = result.scalars().first()
    if not stats:
        raise HTTPException(status_code=404, detail="No statistics available")

    return UserStatisticsOut(
        total_users=stats.total_users,
        average_age=stats.average_age,
        min_age=stats.min_age,
        max_age=stats.max_age,
        eye_color_distribution=stats.eye_color_distribution or {},
        calculated_at=stats.calculated_at,
    )



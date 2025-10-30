from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON as JSONType
from datetime import datetime

from ..db import Base


def _json_type():
    """Return a JSON column type compatible with both Postgres and SQLite.

    Uses JSONB on Postgres for efficiency, falls back to generic JSON otherwise.
    """
    try:
        # JSONB is only available on Postgres; if driver not present at runtime,
        # SQLAlchemy will still allow declaration, but for portability we prefer runtime decision.
        return JSONB
    except Exception:
        return JSONType


class UserStatistics(Base):
    __tablename__ = "user_statistics"

    id = Column(Integer, primary_key=True, index=True)
    calculated_at = Column(DateTime, nullable=False, index=True, default=datetime.utcnow)
    total_users = Column(Integer, nullable=False)
    average_age = Column(Float, nullable=False)
    min_age = Column(Integer, nullable=False)
    max_age = Column(Integer, nullable=False)
    # Use generic JSON type; SQLAlchemy will map to TEXT for SQLite and JSON/JSONB for Postgres
    eye_color_distribution = Column(JSONType, nullable=False)



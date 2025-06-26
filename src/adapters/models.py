# src/adapters/models.py

from sqlalchemy import Column, Enum, JSON, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from adapters.db import Base
from core.models import Player, MatchStatus

class MatchORM(Base):
    __tablename__ = "matches"

    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    board = Column(JSON, nullable=False)
    status = Column(Enum(MatchStatus, name="matchstatus"), nullable=False)
    next_player = Column(
        Enum(Player, name="player"), 
        nullable=True,    
        default=Player.X
    )

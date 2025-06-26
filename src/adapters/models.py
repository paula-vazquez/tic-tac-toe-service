# src/adapters/models.py

import uuid
from sqlalchemy import Column, String, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from adapters.db import Base
from core.models import MatchStatus, Player

class MatchORM(Base):
    __tablename__ = "matches"

    # UUID primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    # Almacena el tablero como JSON (lista de listas de str)
    board = Column(JSON, nullable=False)

    # Estado: in_progress, X_wins, O_wins, draw
    status = Column(Enum(MatchStatus), nullable=False)

    # El siguiente jugador: X u O
    next_player = Column(Enum(Player), nullable=False)

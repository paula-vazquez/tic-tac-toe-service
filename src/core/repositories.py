# src/core/repositories.py

from typing import Protocol
from uuid import UUID
from core.models import Match

class MatchRepository(Protocol):
    """Interfaz que deberá implementar cualquier repositorio de Match."""
    def get(self, match_id: UUID) -> Match:
        ...

    def save(self, match: Match) -> None:
        ...

# src/schemas.py

from pydantic import BaseModel
from uuid import UUID
from typing import List

class CreateResponse(BaseModel):
    matchId: UUID

class SquareIn(BaseModel):
    x: int
    y: int

class MoveRequest(BaseModel):
    matchId: UUID
    playerId: str       # "X" o "O"
    square: SquareIn

class MatchState(BaseModel):
    board: List[List[str]]
    status: str
    next_player: str

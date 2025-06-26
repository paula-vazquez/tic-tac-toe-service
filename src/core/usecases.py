# src/core/usecases.py

from uuid import UUID
from core.models import Match, Player, Square
from core.repositories import MatchRepository

class CreateMatch:
    def __init__(self, repo: MatchRepository):
        self.repo = repo

    def execute(self) -> UUID:
        """
        Crea un nuevo Match con tablero vacío, lo persiste y devuelve su id.
        """
        match = Match()            # constructor de core.models crea tablero 3×3 vacío
        self.repo.save(match)      # persiste (implementado en adapters)
        return match.id

class MakeMove:
    def __init__(self, repo: MatchRepository):
        self.repo = repo

    def execute(self, match_id: UUID, player: Player, square: Square) -> dict:
        """
        Carga el Match, aplica un movimiento (ignora inválidos),
        persiste los cambios y devuelve el estado actualizado.
        """
        match = self.repo.get(match_id)
        match.make_move(player, square)   # lógica en core.models
        self.repo.save(match)
        return match.to_dict()            # serializar a dict para la capa superior

class GetStatus:
    def __init__(self, repo: MatchRepository):
        self.repo = repo

    def execute(self, match_id: UUID) -> dict:
        """
        Recupera el Match y devuelve su estado (board, status, next_player).
        """
        match = self.repo.get(match_id)
        return match.to_dict()

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
import uuid
from typing import List, Optional


class Player(Enum):
    X = "X"
    O = "O"


@dataclass(frozen=True)
class Square:
    x: int  # 1-indexed column (1..3)
    y: int  # 1-indexed row (1..3)


class MatchStatus(Enum):
    IN_PROGRESS = auto()
    DRAW = auto()
    X_WINS = auto()
    O_WINS = auto()


@dataclass
class Match:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    board: List[List[Optional[Player]]] = field(
        default_factory=lambda: [[None for _ in range(3)] for _ in range(3)]
    )
    status: MatchStatus = MatchStatus.IN_PROGRESS
    next_player: Player = Player.X

    def __post_init__(self):
        # Validate board dimensions
        if len(self.board) != 3 or any(len(row) != 3 for row in self.board):
            raise ValueError("Board must be a 3x3 grid")

    def make_move(self, player: Player, square: Square) -> None:
        """
        Intenta colocar la ficha del jugador en la casilla indicada.
        Movimientos inválidos o fuera de turno se ignoran sin alterar el estado.
        """
        # Sólo si el juego sigue en progreso
        if self.status != MatchStatus.IN_PROGRESS:
            return
        # Debe ser el turno correcto
        if player != self.next_player:
            return
        # Ajustar índices a 0-based
        row = square.y - 1
        col = square.x - 1
        # Validar índices dentro de rango
        if not (0 <= row < 3 and 0 <= col < 3):
            return
        # Casilla ya ocupada
        if self.board[row][col] is not None:
            return
        # Realizar movimiento
        self.board[row][col] = player
        # Comprobar victoria o empate
        winner = self._check_winner()
        if winner is not None:
            self.status = MatchStatus.X_WINS if winner == Player.X else MatchStatus.O_WINS
        elif all(all(cell is not None for cell in row_cells) for row_cells in self.board):
            self.status = MatchStatus.DRAW
        else:
            # Cambiar turno
            self.next_player = Player.O if player == Player.X else Player.X

    def _check_winner(self) -> Optional[Player]:
        """
        Revisa filas, columnas y diagonales para determinar si hay un vencedor.
        Devuelve Player.X, Player.O o None.
        """
        b = self.board
        lines = []
        # Filas y columnas
        for i in range(3):
            lines.append([b[i][j] for j in range(3)])  # fila i
            lines.append([b[j][i] for j in range(3)])  # columna i
        # Diagonales
        lines.append([b[i][i] for i in range(3)])
        lines.append([b[i][2 - i] for i in range(3)])
        for line in lines:
            if line[0] is not None and all(cell == line[0] for cell in line):
                return line[0]
        return None

    def to_dict(self) -> dict:
        """
        Serializa el estado de la partida para respuestas JSON.
        """
        return {
            "id": str(self.id),
            "board": [[cell.value if cell else None for cell in row] for row in self.board],
            "status": self.status.name,
            "next_player": self.next_player.value if self.status == MatchStatus.IN_PROGRESS else None
        }

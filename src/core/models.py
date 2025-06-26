# src/core/models.py

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import uuid
from typing import List


class Player(Enum):
    X = "X"
    O = "O"


@dataclass(frozen=True)
class Square:
    x: int  # 1-indexed column (1..3)
    y: int  # 1-indexed row    (1..3)


class MatchStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    DRAW        = "DRAW"
    X_WINS      = "X_WINS"
    O_WINS      = "O_WINS"


@dataclass
class Match:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    # Usamos siempre cadenas; "" para casilla vacía, "X" o "O" para ocupadas.
    board: List[List[str]] = field(
        default_factory=lambda: [["" for _ in range(3)] for _ in range(3)]
    )
    status:      MatchStatus = MatchStatus.IN_PROGRESS
    next_player: Player      = Player.X

    def __post_init__(self):
        # Validar dimensiones del tablero
        if len(self.board) != 3 or any(len(row) != 3 for row in self.board):
            raise ValueError("Board must be a 3x3 grid")

    def make_move(self, player: Player, square: Square) -> None:
        """
        Coloca el símbolo del jugador en la casilla indicada.
        Movimientos inválidos o fuera de turno se ignoran sin alterar el estado.
        """
        if self.status != MatchStatus.IN_PROGRESS:
            return
        if player != self.next_player:
            return

        row = square.y - 1
        col = square.x - 1
        if not (0 <= row < 3 and 0 <= col < 3):
            return

        # Solo permitimos mover si la casilla está vacía ("")
        if self.board[row][col] != "":
            return

        # Realizar movimiento
        self.board[row][col] = player.value

        # Determinar si hay ganador o empate
        winner = self._check_winner()
        if winner is not None:
            self.status = MatchStatus.X_WINS if winner == Player.X.value else MatchStatus.O_WINS
            self.next_player = None  # opcional: no hay turno tras ganar
        elif all(cell != "" for row in self.board for cell in row):
            self.status = MatchStatus.DRAW
            self.next_player = None
        else:
            # Cambiar turno
            self.next_player = Player.O if player == Player.X else Player.X

    def _check_winner(self) -> str | None:
        """
        Revisa filas, columnas y diagonales.
        Devuelve "X", "O" o None.
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
            if line[0] != "" and all(cell == line[0] for cell in line):
                return line[0]

        return None

    def to_dict(self) -> dict:
        """
        Serializa el estado para JSON.
        """
        return {
            "id": str(self.id),
            "board":       self.board,
            "status":      self.status.value,
            "next_player": self.next_player.value if self.next_player else None
        }

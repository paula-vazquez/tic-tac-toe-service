import uuid
import pytest
from core.models import Match, Player, Square, MatchStatus

def test_initial_board_empty_and_turn_X():
    m = Match()
    assert m.status == MatchStatus.IN_PROGRESS
    assert m.next_player == Player.X
    assert all(cell == "" for row in m.board for cell in row)

def test_make_move_places_X_and_switches_to_O():
    m = Match()
    m.make_move(Player.X, Square(x=1, y=1))
    assert m.board[0][0] == "X"
    assert m.next_player == Player.O

def test_cannot_move_same_player_twice_in_row():
    m = Match()
    m.make_move(Player.X, Square(1,1))
    # vuelve a intentar X: no cambia nada
    m.make_move(Player.X, Square(2,1))
    assert m.board[0][1] == ""
    assert m.next_player == Player.O

def test_ignore_move_out_of_bounds():
    m = Match()
    m.make_move(Player.X, Square(0,0))  # fuera de rango
    assert all(cell == "" for row in m.board for cell in row)

def test_detect_horizontal_win():
    m = Match()
    m.board = [["X","X",""], ["","",""], ["","",""]]
    m.next_player = Player.X
    m.make_move(Player.X, Square(3,1))
    assert m.status == MatchStatus.X_WINS

def test_detect_vertical_win():
    m = Match()
    m.board = [["O","",""], ["O","",""], ["","", ""]]
    m.next_player = Player.O
    m.make_move(Player.O, Square(1,3))
    assert m.status == MatchStatus.O_WINS

def test_detect_diagonal_win():
    m = Match()
    m.make_move(Player.X, Square(1,1))
    m.make_move(Player.O, Square(1,2))
    m.make_move(Player.X, Square(2,2))
    m.make_move(Player.O, Square(1,3))
    m.make_move(Player.X, Square(3,3))
    assert m.status == MatchStatus.X_WINS

def test_detect_draw():
    # Rellenamos sin ganador
    seq = [
        (Player.X, Square(1,1)), (Player.O, Square(1,2)),
        (Player.X, Square(1,3)), (Player.O, Square(2,1)),
        (Player.X, Square(2,3)), (Player.O, Square(2,2)),
        (Player.X, Square(3,1)), (Player.O, Square(3,3)),
        (Player.X, Square(3,2)),
    ]
    m = Match()
    for p,s in seq:
        m.make_move(p, s)
    assert m.status == MatchStatus.DRAW

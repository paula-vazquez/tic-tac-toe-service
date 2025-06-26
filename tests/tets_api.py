import pytest
from fastapi.testclient import TestClient
from adapters.db import Base, engine, SessionLocal
from main import app
from adapters.models import MatchORM

# Fixture para limpiar/crear BD de test
@pytest.fixture(autouse=True)
def prepare_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_full_game_flow():
    # 1) Crear partida
    r1 = client.post("/create")
    assert r1.status_code == 200
    match_id = r1.json()["matchId"]

    # 2) Primer movimiento X
    r2 = client.post("/move", json={
        "matchId": match_id,
        "playerId": "X",
        "square": {"x":0, "y":0}
    })
    assert r2.status_code == 200
    state = r2.json()
    assert state["board"][0][0] == "X"
    assert state["next_player"] == "O"

    # 3) Movimiento inválido (X trata de jugar fuera de turno)
    r3 = client.post("/move", json={
        "matchId": match_id,
        "playerId": "X",
        "square": {"x":1, "y":0}
    })
    assert r3.status_code == 400

    # 4) Consultar estado final
    r4 = client.get(f"/status?matchId={match_id}")
    assert r4.status_code == 200
    s = r4.json()
    assert s["board"][0][0] == "X"
    assert s["status"] == "IN_PROGRESS"

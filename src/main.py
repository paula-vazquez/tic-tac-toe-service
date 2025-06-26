# src/main.py

from fastapi import FastAPI, HTTPException, Depends
from uuid import UUID

from core.usecases import CreateMatch, MakeMove, GetStatus
from adapters.sql_match_repository import SQLMatchRepository
from schemas import CreateResponse, MoveRequest, MatchState
from core.models import Player, Square

app = FastAPI(title="Tic-Tac-Toe Service")

# Dependencia para el repositorio
def get_repo():
    return SQLMatchRepository()

@app.post("/create", response_model=CreateResponse)
def create_match(repo=Depends(get_repo)):
    usecase = CreateMatch(repo)
    match_id = usecase.execute()
    return CreateResponse(matchId=match_id)

@app.post("/move", response_model=MatchState)
def move(req: MoveRequest, repo=Depends(get_repo)):
    try:
        # Convierte strings a enums/domain
        player = Player(req.playerId)
        square = Square(req.square.x, req.square.y)
        usecase = MakeMove(repo)
        result = usecase.execute(req.matchId, player, square)
        return MatchState(**result)
    except ValueError as err:
        # Captura errores de lógica
        raise HTTPException(status_code=400, detail=str(err))

@app.get("/status", response_model=MatchState)
def status(matchId: UUID, repo=Depends(get_repo)):
    try:
        usecase = GetStatus(repo)
        result = usecase.execute(matchId)
        return MatchState(**result)
    except Exception as err:
        raise HTTPException(status_code=404, detail="Match no encontrado")

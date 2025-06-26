# src/main.py

import logging
from fastapi import FastAPI, HTTPException, Depends, Request
from uuid import UUID

from core.usecases import CreateMatch, MakeMove, GetStatus
from adapters.sql_match_repository import SQLMatchRepository
from schemas import CreateResponse, MoveRequest, MatchState
from core.models import Player, Square

# 1) Configuración global del logging: va a stderr por defecto
logging.basicConfig(
    level=logging.INFO,  # Nivel mínimo a INFO
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("tictactoe")  

app = FastAPI(title="Tic-Tac-Toe Service")

# 2) Middleware sencillo para loggear cada petición
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"→ {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"← {response.status_code} {request.method} {request.url.path}")
    return response

def get_repo():
    return SQLMatchRepository()

@app.post("/create", response_model=CreateResponse)
def create_match(repo=Depends(get_repo)):
    usecase = CreateMatch(repo)
    match_id = usecase.execute()
    logger.info(f"Created new match: match_id={match_id}")
    return CreateResponse(matchId=match_id)

@app.post("/move", response_model=MatchState)
def move(req: MoveRequest, repo=Depends(get_repo)):
    logger.debug(f"Request move: match_id={req.matchId} player={req.playerId} x={req.square.x} y={req.square.y}")
    try:
        player = Player(req.playerId)
        square = Square(req.square.x, req.square.y)
        usecase = MakeMove(repo)
        result = usecase.execute(req.matchId, player, square)
        logger.info(f"Move applied: match_id={req.matchId} next_player={result['next_player']} status={result['status']}")
        return MatchState(**result)
    except ValueError as err:
        logger.warning(f"Ignored invalid move: match_id={req.matchId} reason={err}")
        raise HTTPException(status_code=400, detail=str(err))

@app.get("/status", response_model=MatchState)
def status(matchId: UUID, repo=Depends(get_repo)):
    logger.debug(f"Status request: match_id={matchId}")
    try:
        usecase = GetStatus(repo)
        result = usecase.execute(matchId)
        logger.info(f"Status returned: match_id={matchId} status={result['status']}")
        return MatchState(**result)
    except Exception:
        logger.error(f"Match not found: match_id={matchId}")
        raise HTTPException(status_code=404, detail="Match no encontrado")

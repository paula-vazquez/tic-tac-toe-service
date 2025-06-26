# src/main.py

import logging
import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from uuid import UUID

from core.usecases import CreateMatch, MakeMove, GetStatus
from adapters.sql_match_repository import SQLMatchRepository
from schemas import CreateResponse, MoveRequest, MatchState
from core.models import Player, Square

# 1) Logging a stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("tictactoe")

app = FastAPI(title="Tic-Tac-Toe Service")

# 2) CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3) Middleware de logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"→ {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"← {response.status_code} {request.method} {request.url.path}")
    return response

# 4) Dependencia del repo
def get_repo():
    return SQLMatchRepository()

# 5) Endpoints API
@app.post("/create", response_model=CreateResponse)
def create_match(repo=Depends(get_repo)):
    match_id = CreateMatch(repo).execute()
    logger.info(f"Created new match: match_id={match_id}")
    return CreateResponse(matchId=match_id)

@app.post("/move", response_model=MatchState)
def move(req: MoveRequest, repo=Depends(get_repo)):
    logger.debug(f"Request move: {req}")
    try:
        player = Player(req.playerId)
        square = Square(req.square.x, req.square.y)
        result = MakeMove(repo).execute(req.matchId, player, square)
        logger.info(f"Move applied: match_id={req.matchId} -> {result}")
        return MatchState(**result)
    except ValueError as err:
        logger.warning(f"Ignored invalid move: match_id={req.matchId} reason={err}")
        raise HTTPException(status_code=400, detail=str(err))

@app.get("/status", response_model=MatchState)
def status(matchId: UUID, repo=Depends(get_repo)):
    logger.debug(f"Status request: match_id={matchId}")
    try:
        result = GetStatus(repo).execute(matchId)
        logger.info(f"Status returned: match_id={matchId} -> {result}")
        return MatchState(**result)
    except Exception:
        logger.error(f"Match not found: match_id={matchId}")
        raise HTTPException(status_code=404, detail="Match no encontrado")

# 6) Servir index.html en '/'
@app.get("/", include_in_schema=False)
def root():
    return FileResponse("frontend/index.html")

# 7) Montar el resto de estáticos en '/static'
if os.path.isdir("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

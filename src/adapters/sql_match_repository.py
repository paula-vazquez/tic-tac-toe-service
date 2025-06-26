# src/adapters/sql_match_repository.py

import logging
from uuid import UUID
from sqlalchemy.orm import Session
from adapters.db import SessionLocal
from adapters.models import MatchORM
from core.models import Match as DomainMatch
from core.repositories import MatchRepository

logger = logging.getLogger("tictactoe.repository")

class SQLMatchRepository(MatchRepository):
    def __init__(self):
        # Factory de sesiones
        self._SessionLocal = SessionLocal

    def get(self, match_id: UUID) -> DomainMatch:
        logger.debug(f"DB GET match_id={match_id}")
        db: Session = self._SessionLocal()
        try:
            orm = db.query(MatchORM).filter(MatchORM.id == match_id).one()
            m = DomainMatch(id=orm.id)
            m.board = [
                [cell if cell is not None else "" for cell in row]
                for row in orm.board
            ]
            m.status = orm.status
            m.next_player = orm.next_player
            logger.debug(f"DB GET success: match_id={match_id}")
            return m
        except Exception as e:
            logger.error(f"DB GET error: match_id={match_id} error={e}")
            raise
        finally:
            db.close()

    def save(self, match: DomainMatch) -> None:
        logger.debug(f"DB SAVE match_id={match.id}")
        db: Session = self._SessionLocal()
        try:
            orm = db.query(MatchORM).filter(MatchORM.id == match.id).one_or_none()
            if orm is None:
                orm = MatchORM(
                    id=match.id,
                    board=match.board,
                    status=match.status,
                    next_player=match.next_player,
                )
                db.add(orm)
            else:
                orm.board = match.board
                orm.status = match.status
                orm.next_player = match.next_player
            db.commit()
            logger.debug(f"DB SAVE committed: match_id={match.id}")
        except Exception as e:
            logger.error(f"DB SAVE error: match_id={match.id} error={e}")
            db.rollback()
            raise
        finally:
            db.close()

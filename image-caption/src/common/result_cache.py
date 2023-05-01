import hashlib
from abc import ABC
from typing import Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select, Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DeclarativeBase = declarative_base()


class CachedResult(DeclarativeBase):
    __tablename__ = 'cache'

    id = Column(Integer, primary_key=True)
    digest = Column(String(32), nullable=False, unique=True)
    result = Column(String, nullable=False)


class ResultCacheAbstract(ABC):
    @staticmethod
    def calc_digest(*args: bytes | bytearray | str) -> str:
        pass

    def get(self, digest: str) -> Optional[str]:
        pass

    def put(self, digest: str, result: str):
        pass


class ResultCache(ResultCacheAbstract):
    def __init__(self, engine: Engine):
        self.engine = engine

    @staticmethod
    def calc_digest(*args: bytes | bytearray | str) -> str:
        hasher = hashlib.md5(usedforsecurity=False)

        for arg in args:
            if isinstance(arg, str):
                hasher.update(arg.encode('utf-8'))
            elif arg is None:
                continue
            else:
                hasher.update(arg)

        return hasher.hexdigest()

    def get(self, digest: str) -> Optional[str]:
        stmt = select(CachedResult).where(CachedResult.digest == digest)
        session_maker: sessionmaker = sessionmaker(self.engine,
                                                   expire_on_commit=False,
                                                   class_=Session)
        with session_maker() as session:
            session: Session
            result: Optional[CachedResult] = session.execute(stmt).one_or_none()

            if result is None:
                return None

            return result[0].result

    def put(self, digest: str, result: str):
        stmt = select(CachedResult).where(CachedResult.digest == digest)
        session_maker: sessionmaker = sessionmaker(self.engine,
                                                   expire_on_commit=False,
                                                   class_=Session)
        with session_maker() as session:
            session: Session
            queried: Optional[CachedResult] = session.execute(stmt).one_or_none()

            to_save: CachedResult
            if queried is None:
                to_save = CachedResult(
                    digest=digest,
                    result=result
                )
            else:
                to_save = queried[0]
                to_save.result = result
            session.add(to_save)
            session.commit()


class ResultCacheStub(ResultCacheAbstract):
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def calc_digest(*args: bytes | bytearray | str) -> str:
        return '00000000000000000000000000000000'

    def get(self, digest: str) -> Optional[str]:
        return None

    def put(self, digest: str, result: str):
        pass

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from core.config import settings


class Database:
    def __init__(self, url: str, poolclass=None):
        self.engine = create_async_engine(
            url=url,
            poolclass=poolclass,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session


db_helper = Database(url=settings.db_url)

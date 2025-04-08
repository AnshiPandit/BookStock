from sqlmodel import create_engine, text, SQLModel
# Engine manages database connections and executes raw SQL.
# using async engine coz we are using async engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.models import Book
from sqlalchemy.orm import sessionmaker

from src.config import Config

async_engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,
    connect_args={"ssl": "require"}
)

# this func allows to create connectin to db and keep that connection for as long as the app is running
async def init_db():
    async with async_engine.begin() as conn:
        # statement = text("SELECT 'hello';")
        # result = await conn.execute(statement)
        # print(result.all())

        # to implement the CRUD operation
        await conn.run_sync(SQLModel.metadata.create_all)

# we need session class 
async def get_session() -> AsyncSession:
    
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session # will return the session
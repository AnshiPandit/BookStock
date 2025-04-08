from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import date, datetime
import uuid

# copy from schemas.py and sql model is very similar to pydantic model
class Book(SQLModel, table=True):
    __tablename__ = "books"
    
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    """
        Use sa_column when:
        You need database-specific types (e.g., pg.UUID for PostgreSQL).
        You want custom SQLAlchemy behavior, like adding constraints.
        You need compatibility with raw SQLAlchemy code.
    """
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    # Postgresql timesatamps createion, so no need to enter it manually
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
# uid are diff from pimary key as it uses more storage and is non-sequential in nature
    
    # The __repr__ method is a special method in Python that provides a string representation of an object. It is useful for debugging and logging.
    def __repr__(self):
        return f"<Book {self.title}>"
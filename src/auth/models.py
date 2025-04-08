from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import date, datetime
import uuid 

# User class uses SQLModel class and it is a table so table=True
class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username : str
    email : str
    firstname : str
    lastname : str
    is_verified : bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))

    def __repr__(self):
        return f"<User {self.username}>"
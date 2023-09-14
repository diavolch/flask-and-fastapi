import datetime
import databases
import sqlalchemy
from pydantic import BaseModel, Field
from sqlalchemy import ForeignKey

DATABASE_URL = 'sqlite:///db.db'
db = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": True})
metadata.create_all(engine)


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(20)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(128)),
)

items = sqlalchemy.Table(
    "items",
    metadata,
    sqlalchemy.Column("item_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(50)),
    sqlalchemy.Column("description", sqlalchemy.String(128)),
    sqlalchemy.Column("price", sqlalchemy.Integer),
)


orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("order_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey('users.user_id')),
    sqlalchemy.Column("item_id", sqlalchemy.Integer, ForeignKey('items.item_id')),
    sqlalchemy.Column("created_on", sqlalchemy.DATETIME, default=datetime.datetime.now())
)


class Users(BaseModel):
    user_id: int
    name: str = Field(..., title='Name', min_length=4, max_length=20)
    email: str = Field(..., title="Email", max_length=128)
    password: str = Field(..., title="Password", max_length=128)


class Items(BaseModel):
    item_id: int
    title: str = Field(..., title='Title', min_length=4, max_length=20)
    description: str = Field(title="Description", max_length=128)
    price: float = Field(title="Price", default=0)


class Orders(BaseModel):
    order_id: int
    user_id: int
    item_id: int


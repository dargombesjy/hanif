from sqlalchemy import Date, Table, Column, Integer, String, Boolean, \
    Date, ForeignKey, Float
from app.models import metadata_obj

base_menu = Table(
    "base_menu",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('code', String),
    Column('parent', String),
    Column('path', String),
)

base_config = Table(
    "base_config",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String)
)
from sqlalchemy import Date, Table, Column, Integer, String, Boolean, \
    Date, ForeignKey, Float
from app.models import metadata_obj


auth_group = Table(
    "auth_group",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
)

auth_object = Table(
    "auth_object",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('code', String),
    Column('object', String),
    Column('object_name', String),
)

auth_object_assign = Table(
    "auth_object_assign",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('auth_group_id', Integer, ForeignKey('auth_group.id')),
    Column('auth_object_id', Integer, ForeignKey('auth_object.id')),
    Column('access_level', String),
)

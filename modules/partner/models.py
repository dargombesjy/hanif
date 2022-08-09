from sqlalchemy import Date, Table, Column, Integer, String, Boolean, \
    Date, ForeignKey, Float
from app.models import metadata_obj

partner = Table(
    "partner",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
)
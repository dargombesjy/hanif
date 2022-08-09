from sqlalchemy import Date, Table, Column, Integer, String, Boolean, \
    Date, ForeignKey, Float
from app.models import metadata_obj


account_group = Table(
    "account_group",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('parent_id', Integer, nullable=True),
    Column('parent_path', String),
)

account_type = Table(
    "account_type",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('group', String),
    Column('type', String),
    Column('account_type', String),
    Column('include_initial_balance', Boolean),
)

account = Table(
    "account",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('group', String),
    Column('account_type', String),
)

account_journal = Table(
    "account_journal",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('code', String),
    Column('type', String),
    Column('journal_type', String(10)),
    Column('debit_account_id', Integer, ForeignKey('account.id')),
    Column('credit_account_id', Integer, ForeignKey('account.id')),
    Column('currency', String),
)

account_move = Table(
    "account_move",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('ref', String),
    Column('date', Date),
    Column('journal_id', Integer, ForeignKey('account_journal.id')),
    Column('partner_id', Integer, ForeignKey('partner.id')),
    Column('amount', Float(precision=17)),
    Column('balance', Float(precision=17)),
    Column('currency', String),
)

account_move_line = Table(
    "account_move_line",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('account_move_id', Integer, ForeignKey('account_move.id')),
    Column('indicator', String(1)),
    Column('amount', Float(precision=17)),
    Column('currency', String),
    Column('account_id', Integer, ForeignKey('account.id')),
    Column('invoice_id', Integer, ForeignKey('account_invoice.id')),
)

account_invoice = Table(
    "account_invoice",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('invoice_date', Date),
    Column('post_date', Date),
    Column('partner_id', Integer, ForeignKey('partner.id')),
    Column('amount', Float(precision=17)),
    Column('discount', Float(precision=17)),
    Column('residual', Float(precision=17)),
    Column('currency', String),
)

account_invoice_line = Table(
    "account_invoice_line",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('qty', Float(precision=17)),
    Column('price', Float(precision=17)),
    Column('currency', String),
)
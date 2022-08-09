from app.db import Manager
from wtforms import Form, FieldList,HiddenField, IntegerField, StringField, DateField, \
    DecimalField, SelectField, FormField

class Account(Manager):
    _table = 'account'


class AccountJournal(Manager):
    _table = 'account_journal'


class AccountMove(Manager):
    _table = 'account_move'

    def create(self, **kwargs):
        lines = kwargs.pop('lines')
        with self.engine.connect() as conn:
            stmt = self.insert(**kwargs)
            res = conn.execute(stmt)

            move_line = AccountMoveLine()
            for line in lines:
                line['account_move_id'] = res.inserted_primary_key[0]
                stmt = move_line.insert(**line)
                conn.execute(stmt)

            conn.commit()

        return res

    @classmethod
    def create_form(cls):
        lines_form = AccountMoveLine.create_form()
        class AccountMoveForm(Form):
            id = HiddenField('id')
            name = StringField('Name')
            ref = StringField('Ref.')
            date = DateField('Doc. Date')
            journal_id = SelectField(
                'Journal', coerce=int, choices=cls.get_related('account_journal'),)
            partner_id = SelectField('Partner', coerce=int, choices=cls.get_related('account_journal'),)
            lines = FieldList(FormField(lines_form), min_entries=2)

        return AccountMoveForm


class AccountMoveLine(Manager):
    _table = 'account_move_line'

    @classmethod
    def create_form(cls):
        class AccountMoveLineForm(Form):
            id = HiddenField('id')
            name = StringField('Name')
            account_move_id = IntegerField('Move')
            indicator = StringField('Debit/Credit Indicator')
            amount = DecimalField('Amount')
            currency = StringField('Currency')
            account_id = SelectField(
                'Account', coerce=int, choices=cls.get_related('account'))
            invoice_id = SelectField(
                'Invoice', coerce=int, choices=cls.get_related('account_invoice'))

        return AccountMoveLineForm

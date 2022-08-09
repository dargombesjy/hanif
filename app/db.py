from itertools import chain
import logging
from sqlalchemy import create_engine, delete, insert, select, update, and_, or_, not_, func, \
    Integer, Date, Float
from utils.filter import build_filters
from wtforms import Form, IntegerField, StringField, DateField, DecimalField, \
    SubmitField, validators


class Manager(object):

    env = None

    def __init__(self):
        self.engine = create_engine('postgresql://warno006089:markesot!23@localhost:5432/myapp', future=True)  # echo=True)
        # self.form = self.create_form()
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        
    def create(self, **kwargs):
        with self.engine.connect() as conn:
            stmt = self.insert(kwargs)
            res = conn.execute(stmt)
            self.after_create(res)
            conn.commit()
        return res

    def read(self, filter_spec=None):
        table = self._get_table()
        tables = [table]   # [self._table]
        joins = []
        for col in table.c:   # self._table.c:
            if col.foreign_keys:
                t_ = list(col.foreign_keys)[0].column.table
                tables.append(t_)
                joins.append(t_)

        stmt = select(*tables)
        if len(joins) > 1:
            for j in joins:
                stmt = stmt.join(j)

        if filter_spec:
            for filter in build_filters(filter_spec):
                clause = filter.build(table)   #self._table)
            stmt = stmt.where(clause)

        with self.engine.connect() as conn:
            res = conn.execute(stmt)
        return res

    def update(self, pk, **kwargs):
        with self.engine.begin() as conn:
            # stmt = update(self._table).where(self._table.c.id == pk).values(data)\
            #     .returning(self._table.c.id)
            stmt = self.change(pk, **kwargs)
            conn.execute(stmt)

    def delete(self, pk):
        table = self._get_table()
        with self.engine.begin() as conn:
            stmt = delete(table).where(table.c.id == pk)   # (self._table).where(self._table.c.id == pk)
            conn.execute(stmt)

    def after_create(self, res):
        pass

    def insert(self, **kwargs):
        table = self._get_table()
        data = self._validate_field(kwargs)
        return insert(table).values(data)   # (self._table).values(data)

    def change(self, pk, **kwargs):
        table = self._get_table()
        data = self._validate_field(kwargs)
        return update(table).where(table.c.id == pk).values(data)\
                .returning(self._table.c.id)
    
    def _get_table(self):
        m = self.__module__.split('.')
        modname = '{}.{}'.format(m[0], m[1])
        module = self.env.get_module(modname)
        return getattr(module.models, self._table, False)


    def _validate_field(self, **kwargs):
        return kwargs

    @classmethod
    def get_related(self, tablename):
        return [(1, 'Test')]

    @classmethod
    def create_form(cls):
        class StaticForm(Form):
            pass
            # submit = SubmitField()

        for c in cls._table.c:
            type_ = StringField
            if isinstance(c.type, Integer):
                type_ = IntegerField
            elif isinstance(c.type, Date):
                type_ = DateField
            elif isinstance(c.type, Float):
                type_ = DecimalField

            setattr(StaticForm, c.key, type_(c.description))
        return StaticForm

    # def create_form(self):
    #     attributes = dict()
    #     for c in self._table.c:
    #         type_ = StringField
    #         if isinstance(c.type, Integer):
    #             type_ = IntegerField
    #         elif isinstance(c.type, Date):
    #             type_ = DateField
    #         elif isinstance(c.type, Float):
    #             type_ = DecimalField

    #         attributes[c.key] = type_(c.name)
    #     return type('ModelForm', (Form,), attributes)

    # def read(self, filter_spec=None):
    #     stmt = select(self._table)
    #     if filter_spec:
    #         for filter in build_filters(filter_spec):
    #             clause = filter.build(self._table)
    #         stmt = select(self._table).where(clause)

    #     with self.engine.connect() as conn:
    #         res = conn.execute(stmt)
    #     return res

    # def read_subquery(self, filter_spec=None):
    #     pass
from collections import namedtuple
# from collections.abc import Iterable
# from utils import string_types
from itertools import chain
from inspect import signature
from sqlalchemy import and_, or_, not_, func

BooleanFunction = namedtuple(
    'BooleanFunction', ('key', 'sqlalchemy_fn', 'only_one_arg')
)
BOOLEAN_FUNCTIONS = [
    BooleanFunction('or', or_, False),
    BooleanFunction('and', and_, False),
    BooleanFunction('not', not_, True),
]
"""
Sqlalchemy boolean functions that can be parsed from the filter definition.
"""


class Operator(object):

    OPERATORS = {
        'is_null': lambda f: f.is_(None),
        'is_not_null': lambda f: f.isnot(None),
        '==': lambda f, a: f == a,
        'eq': lambda f, a: f == a,
        '!=': lambda f, a: f != a,
        'ne': lambda f, a: f != a,
        '>': lambda f, a: f > a,
        'gt': lambda f, a: f > a,
        '<': lambda f, a: f < a,
        'lt': lambda f, a: f < a,
        '>=': lambda f, a: f >= a,
        'ge': lambda f, a: f >= a,
        '<=': lambda f, a: f <= a,
        'le': lambda f, a: f <= a,
        'like': lambda f, a: f.like(a),
        'ilike': lambda f, a: f.ilike(a),
        'not_ilike': lambda f, a: ~f.ilike(a),
        'in': lambda f, a: f.in_(a),
        'not_in': lambda f, a: ~f.in_(a),
        'any': lambda f, a: f.any(a),
        'not_any': lambda f, a: func.not_(f.any(a)),
    }
    def __init__(self, operator=None):
        if not operator:
            operator = '=='

        if operator not in self.OPERATORS:
            raise Exception('Operator `{}` not valid.'.format(operator))

        self.operator = operator
        self.function = self.OPERATORS[operator]
        self.arity = len(signature(self.function).parameters)


class Filter(object):

    def __init__(self, filter_spec):
        self.filter_spec = filter_spec
        self.operator = Operator(filter_spec[1])
        # value_present = True if len(filter_spec) < 3 else False
        # if not value_present and self.operator.arity == 2:
        #     raise Exception('provide filter value.')
        if self.operator.arity == 2 and len(filter_spec) < 3:
            raise Exception('You must provide a filter value.')
        # if self.operator.arity == 2:
        self.column = filter_spec[0]
        self.get_value(filter_spec[2])
    
    def get_value(self, filter_value):
        self.value = filter_value
        if self.operator.operator == 'ilike':
            self.value = '%{}%'.format(filter_value)

    def build(self, table):
        operator = self.operator
        col = self.column
        value = self.value
        function = operator.function
        arity = operator.arity

        if arity == 1:
            return function(table.c[col])

        if arity == 2:
            return function(table.c[col], value)


class BooleanFilter(object):

    def __init__(self, function, *args):
        self.function = function
        self.filters = args

    def build(self, table):
        return self.function(*[
            filter.build(table) for filter in self.filters
        ])


def _is_iterable_filter(filter_spec):
    """ `filter_spec` may be a list of nested filter specs, or a dict.
    """
    return (
        isinstance(filter_spec, list) and
        not isinstance(filter_spec, tuple)
    )
    # return (
    #     isinstance(filter_spec, Iterable) and
    #     not isinstance(filter_spec, (string_types, dict))
    # )

def build_filters(filter_spec):
    """ Recursively process `filter_spec` """

    if _is_iterable_filter(filter_spec):
        return list(chain.from_iterable(
            build_filters(item) for item in filter_spec
        ))

    # if isinstance(filter_spec, string_types):
    for boolean_func in BOOLEAN_FUNCTIONS:
        if boolean_func.key in filter_spec:   # and not boolean_func.only_one_arg:
            indx = filter_spec.index(boolean_func.key)
            fn_args = filter_spec[indx + 1]

            if not _is_iterable_filter(fn_args):
                    raise Exception(
                        '`{}` value must be an iterable across the function '
                        'arguments'.format(boolean_func.key)
                    )

            if boolean_func.only_one_arg and len(fn_args) != 1:
                raise Exception(
                    '`{}` must have one argument'.format(
                        boolean_func.key
                    )
                )
            if not boolean_func.only_one_arg and len(fn_args) < 1:
                raise Exception(
                    '`{}` must have one or more arguments'.format(
                        boolean_func.key
                    )
                )

            return [
                BooleanFilter(
                    boolean_func.sqlalchemy_fn, *build_filters(fn_args)
                )
            ]

    return [Filter(filter_spec)]
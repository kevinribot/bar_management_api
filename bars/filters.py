from django_filters.rest_framework import FilterSet, CharFilter, BooleanFilter

from .models import Reference, Stock


class StockFilter(FilterSet):
    """
    Filter of the view: 'Stock'
    """

    ref = CharFilter(field_name='reference__ref')
    name = CharFilter(field_name='reference__name')

    class Meta:
        model = Stock
        fields = ['ref', 'name', 'stock']


class MenuFilter(FilterSet):
    """
    Filter of the view: 'Menu'
    'is_available' : Returns references in stock.
    """

    def filter_available(self, name, value):
        if value:
            return self.filter(**{name + '__gt': 0})
        else:
            return self.filter(**{name: 0})

    is_available = BooleanFilter(field_name='total_stock', method=filter_available)

    class Meta:
        model = Reference
        fields = ['ref', 'name', 'is_available']


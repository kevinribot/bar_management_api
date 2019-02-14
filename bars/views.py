from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from .serializers import ReferenceSerializer, BarSerializer, StockSerializer, MenuSerializer, OrderSerializer, OrderItemSerializer, RankSerializer
from .models import Reference, Bar, Stock, Order
from .permissions import OnlyUserAndStaffPermission, PostByClientAndGetByUserPermission
from .filters import StockFilter, MenuFilter

class ReferenceList(generics.ListCreateAPIView):
    """
    get:
    Return the list of references.

    post:
    Create or update a reference.
    """

    queryset = Reference.objects.filter()
    serializer_class = ReferenceSerializer

    permission_classes = (OnlyUserAndStaffPermission,)

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = ('ref', 'name')
    filter_fields = ('ref', 'name')


class BarList(generics.ListCreateAPIView):
    """
    get:
    Returns the list of bars.

    post:
    Create or update a bar.
    """

    queryset = Bar.objects.all()
    serializer_class = BarSerializer

    permission_classes = (OnlyUserAndStaffPermission,)

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = '__all__'
    filter_fields = '__all__'


class StockList(generics.ListCreateAPIView):
    """
    get:
    Returns the inventory list.
    post:
    Create or update stock
    """
	
    queryset = Stock.objects.all().select_related('reference') 
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(bar=self.kwargs.get('bar', 0))
	
    permission_classes = (OnlyUserAndStaffPermission,)
    serializer_class = StockSerializer

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    filter_class = StockFilter
    ordering_fields = ('reference__ref', 'reference__name', 'reference__description', 'stock')


class MenuList(generics.ListAPIView):
    """
    get:
    Returns the availability of references.
    If the bar is specified then the list will limit it to this one.
    """

    serializer_class = MenuSerializer

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    filter_class = MenuFilter
    ordering_fields = ('ref', 'name', 'description')

    queryset = Reference.objects.all()
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if 'bar' in self.kwargs:
            return queryset.filter(stocks__bar__pk=self.kwargs.get('bar', 0))
        else:
            return queryset

    def get_serializer_context(self):
        return {'bar': self.kwargs.get('bar', 0)}


class OrderList(generics.ListAPIView):
    """
    get:
    Returns the list of the orders.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = (OnlyUserAndStaffPermission,)


class OrderDetail(generics.RetrieveAPIView, generics.CreateAPIView):
    """
    get:
    Returns the command corresponding to the specified identifier.
    post:
    Makes an order at the specified bar.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = (PostByClientAndGetByUserPermission,)

    def create(self, validated_data, pk, **kwargs):
        dict_items = dict(self.request.data)
        bar = pk

        # Recording of the order
        order = Order.objects.create(bar=Bar.objects.filter(pk=bar).first())

        # Recovery of the list of references
        for itemRef in list(dict_items.get('items')):
            # Recovery of reference in to database
            reference = Reference.objects.filter(ref=itemRef.get('ref')).first()
            if reference is not None:
                # The reference exists
                cust_req_data_orderitem = {
                    'reference': reference.pk,
                    'order': order.pk
                }

                # Check of stocks
                stock = Stock.objects.filter(reference=reference.pk, bar=bar).first()
                if stock is not None:
                    if stock.stock > 0:
                        # Saving items from the order
                        orderitem_serializer = OrderItemSerializer(data=cust_req_data_orderitem)
                        if orderitem_serializer.is_valid():
                            orderitem_serializer.save()
                    else:
                        # The reference isn't in stock
                        print("La référence '{0}' n'est pas en stock.".format(itemRef.get('ref'), ))
                else:
                    # The reference is not available in this bar
                    print("La référence '{0}' n'est pas disponible dans ce comptoir.".format(itemRef.get('ref'), ))
            else:
                # The reference does not exist
                print("La référence '{0}' n'existe pas.".format(itemRef.get('ref'), ))

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


class RankList(generics.ListAPIView):
    """
    get:
    Returns informations about bars.
    """
    serializer_class = RankSerializer
    queryset = None

    permission_classes = (OnlyUserAndStaffPermission,)
    pagination_class = None

    def get_queryset(self):
        # Recovery of the list of bars that have all the references in stock
        bars_all = Bar.objects.exclude(stocks__stock=0).distinct()
        data_all = {
            'name': 'all_stocks',
            'description': 'Liste des comptoirs qui ont toutes les références en stock.',
            'bars': (bar.pk for bar in bars_all)
        }

        # Recovery of the list of bars that at least one exhausted references
        bars_miss = Bar.objects.filter(stocks__stock=0).distinct()
        data_miss = {
            'name': 'miss_at_least_one',
            'description': 'Liste des comptoirs qui ont au moins une références épuisée.',
            'bars': (bar.pk for bar in bars_miss)
        }

        # Recovery the bar with the most ordered pints
        bar_most = Bar.objects.annotate(total_order=Count('orders__orderItems')).order_by('-total_order').first()
        data_most = {
            'name': 'most_pints',
            'description': 'Liste le comptoir avec le plus de pintes commandées.',
            'bars': [bar_most.pk]
        }

        # Creation of the response
        cust_data_rank = list()
        cust_data_rank.append(data_all)
        cust_data_rank.append(data_miss)
        cust_data_rank.append(data_most)

        rank_serializer = RankSerializer(data=cust_data_rank, many=True)
        rank_serializer.is_valid(raise_exception=True)

        return rank_serializer.data


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count

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
    permission_classes = (OnlyUserAndStaffPermission,)
    serializer_class = StockSerializer

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    filter_class = StockFilter
    ordering_fields = ('reference__ref', 'reference__name', 'reference__description', 'stock')

    # Returns the inventory list of the selected bar.
    def get_queryset(self):
        return Stock.objects.filter(bar=self.kwargs['bar'])

    def perform_create(self, serializer):
        serializer.save(bar=Bar.objects.filter(pk=self.kwargs['bar']).first())


class MenuList(generics.ListAPIView):
    """
    get:
    Returns the availability of references.
    If the bar is specified then the list will limit it to this one.
    """

    queryset = Reference.objects.all()
    serializer_class = MenuSerializer

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    filter_class = MenuFilter
    ordering_fields = ('ref', 'name', 'description')

    # Add all the stocks of a reference to find out the total quantity.
    def get_queryset(self):
        if 'bar' in self.kwargs:
            return Reference.objects.filter(stocks__bar__pk=self.kwargs['bar']).annotate(
                total_stock=Sum('stocks__stock')
            )
        else:
            return Reference.objects.annotate(
                total_stock=Sum('stocks__stock')
            )


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
        cust_req_data_order = {'bar': bar}

        order_serializer = OrderSerializer(data=cust_req_data_order)
        if order_serializer.is_valid():
            order_serializer.save()

        # Recovery of the list of references
        list_items = list()
        for itemRef in list(dict_items.get("items")):
            # Recovery of reference in to database
            reference = Reference.objects.filter(ref=itemRef.get("ref")).first()

            if reference is not None:
                # The reference exists
                cust_req_data_orderitem = {
                    'reference': reference.pk,
                    'order': order_serializer.data.get("pk")
                }

                # Check of stocks
                stock = Stock.objects.filter(reference=reference.pk, bar=bar).first()

                if len(stock) == 1:
                    if stock.stock > 0:
                        # The reference is in stock
                        list_items.append({
                            "ref": reference.ref,
                            "name": reference.name,
                            "description": reference.description}
                        )

                        stock.stock = stock.stock - 1

                        # Update of stocks to database
                        stock_serializer = StockSerializer(stock, data={'stock': stock.stock}, partial=True)
                        if stock_serializer.is_valid():
                            stock_serializer.save()

                        # Saving items from the order
                        orderitem_serializer = OrderItemSerializer(data=cust_req_data_orderitem)
                        if orderitem_serializer.is_valid():
                            orderitem_serializer.save()
                    else:
                        # The reference isn't in stock
                        list_items.append({
                            "ref": itemRef.get("ref"),
                            "description": "La référence n'est pas en stock."
                        })
                else:
                    # The reference is not available in this bar
                    list_items.append({
                        "ref": itemRef.get("ref"),
                        "description": "La référence demandée n'est pas disponible dans ce comptoir."
                    })
            else:
                # The reference does not exist
                list_items.append({
                    "ref": itemRef.get("ref"),
                    "description": "La référence demandée n'existe pas."
                })

        # Creation of the response
        response = {
            "pk": order_serializer.data.get("pk"),
            'items': list_items
        }

        return Response(response, status=status.HTTP_201_CREATED)


class RankList(generics.ListAPIView):
    """
    get:
    Returns informations about bars.
    """
    serializer_class = RankSerializer

    permission_classes = (OnlyUserAndStaffPermission,)
    pagination_class = None

    def get_queryset(self):
        response = list()

        # Recovery of the list of bars that have all the references in stock
        bars_all = Bar.objects.exclude(stocks__stock=0).distinct()
        response_all = {
            'name': 'all_stocks',
            'description': 'Liste des comptoirs qui ont toutes les références en stock.',
            'bars': (bar.pk for bar in bars_all)
        }

        # Recovery of the list of bars that at least one exhausted references
        bars_miss = Bar.objects.filter(stocks__stock=0).distinct()
        response_miss = {
            'name': 'miss_at_least_one',
            'description': 'Liste des comptoirs qui ont au moins une références épuisée.',
            'bars': (bar.pk for bar in bars_miss)
        }

        # Recovery the bar with the most ordered pints
        bar_most = Bar.objects.annotate(total_order=Count('orders__orderItems')).order_by('-total_order').first()
        response_most = {
            'name': 'most_pints',
            'description': 'Liste le comptoir avec le plus de pintes commandées.',
            'bars': [bar_most.pk]
        }

        # Creation of the response
        response.append(response_all)
        response.append(response_miss)
        response.append(response_most)

        return response


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count

from .models import Reference, Bar, Stock, Order, OrderItem
from .serializers import ReferenceSerializer, BarSerializer, StockSerializer, MenuSerializer,  OrderSerializer, OrderCreateSerializer, OrderDetailSerializer, OrderItemSerializer, RankSerializer
from .permissions import OnlyUserAndStaffPermission, OnlyClientPermission
from .filters import StockFilter, MenuFilter


class ReferenceList(generics.ListCreateAPIView):
    """
    get:
    Retourne la liste des références.
    
    post:
    Permet d'ajouter une référence.
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
    Retourne la liste des compteoirs.
    
    post:
    Permet d'ajouter un comptoir.
    """
    queryset = Bar.objects.all()
    serializer_class = BarSerializer

    permission_classes = (OnlyUserAndStaffPermission,)

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = ('id', 'name')
    filter_fields = ('id', 'name')


class StockList(generics.ListAPIView):
    """
    get:
    Retourne la liste des stocks.
    """
    serializer_class = StockSerializer

    permission_classes = (OnlyUserAndStaffPermission,)

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    filter_class = StockFilter
    ordering_fields = ('reference__ref', 'reference__name', 'reference__description', 'stock')

    def get_queryset(self):
        return Stock.objects.filter(bar=self.kwargs['bar'])


class MenuList(generics.ListAPIView):
    """
    get:
    Retourne la liste des stocks pour chaque référence.
    Si le comptoir est précisé alors la liste ce limitera à celui-ci.
    """
    queryset = Reference.objects.all()
    serializer_class = MenuSerializer

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    filter_class = MenuFilter
    ordering_fields = ('ref', 'name', 'description')

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
    Retourne la liste des commandes.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = (OnlyUserAndStaffPermission,)


class OrderCreate(generics.CreateAPIView):
    """
    post:
    Permet de passer une commande à un comptoir.
    """
    serializer_class = OrderCreateSerializer

    permission_classes = (OnlyClientPermission,)

    def create(self, validated_data, bar):
        dict_items = dict(self.request.data)

        # Enregistrement de la commandes
        cust_req_data_order = {'bar': bar}
        
        order_serializer = OrderSerializer(data=cust_req_data_order)
        if order_serializer.is_valid():
            order_serializer.save()

        # Récupération de la liste des références
        lict_items = list()
        for itemRef in list(dict_items.get("items")):
            # Récupération de la référence
            references = Reference.objects.filter(ref=itemRef.get("ref"))
            if len(references) == 1:
                # La référence éxiste
                # Vérification des stocks
                stocks = Stock.objects.filter(reference=references[0].pk, bar=bar)

                if len(stocks) == 1:
                    if stocks[0].stock > 0 :
                        # La bière est en stock - a faire la supression du stock
                        lict_items.append({"ref": references[0].ref,
                                           "name": references[0].name,
                                           "description": references[0].description})

                        stocks[0].stock = stocks[0].stock - 1

                        # Mise à jour des stocks en base de données
                        stock_serializer = StockSerializer(stocks[0], data={'stock': stocks[0].stock}, partial=True)
                        if stock_serializer.is_valid():
                            stock_serializer.save()

                        # Enregistrement des items de la commandes
                        cust_req_data_orderitem = {'reference': references[0].pk, 'order': order_serializer.data.get("id")}
                        orderitem_serializer = OrderItemSerializer(data=cust_req_data_orderitem)
                        if orderitem_serializer.is_valid():
                            orderitem_serializer.save()
                    else:
                        # La bière n'est plus en stock
                        lict_items.append({"ref": itemRef.get("ref"), "description": "La bière n'est plus disponible."})
                else:
                    # "La bière n'est pas disponible à ce comptoire
                    lict_items.append({"ref": itemRef.get("ref"), "description": "La bière n'est pas disponible à ce comptoire."})
            else:
                # La bière n'existe pas
                lict_items.append({"ref": itemRef.get("ref"), "description": "La référence demandée n'existe pas."})
        
        # Création de la response
        response = {"pk": order_serializer.data.get("id")}
        response['items'] = lict_items

        return Response(response)


class OrderDetail(generics.RetrieveAPIView):
    """
    get:
    Retourne la commande correspondant à l'identifiant précisé.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    permission_classes = (OnlyUserAndStaffPermission,)


class RankList(generics.ListAPIView):
    """
    get:
    Retourne le classement des comptoires si la personne est authtifié.
    """
    serializer_class = RankSerializer

    permission_classes = (OnlyUserAndStaffPermission,)
    pagination_class = None

    def get_queryset(self):
        response = list()

        # Recovery of the list of bars that have all the references in stock
        bars_all = Bar.objects.exclude(stocks__stock=0).distinct()
        response_all = {'name': 'all_stocks',
                        'description': 'Liste des comptoirs qui ont toutes les références en stock.',
                        'bars': (bar.pk for bar in bars_all)}

        # Recovery of the list of bars that at least one exhausted references
        bars_miss = Bar.objects.filter(stocks__stock=0).distinct()
        response_miss = {'name': 'miss_at_least_one',
                         'description': 'Liste des comptoirs qui au moins une références éppuisée.',
                         'bars': (bar.pk for bar in bars_miss)}
        
        # Recovery the bar with the most ordered pints
        bar_most = Bar.objects.annotate(total_order=Count('orders__orderItems')).order_by('-total_order').first()
        response_most = {'name': 'most_pints',
                         'description': 'Liste le comptoir avec le plus de pintes commandées.',
                         'bars': [bar_most.pk]}

        # Creation of the response
        response.append(response_all)
        response.append(response_miss)
        response.append(response_most)

        return response


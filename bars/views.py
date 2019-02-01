from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count

from .serializers import *
from .permissions import OnlyUserAndStaffPermission, PostByClientAndGetByUserPermission
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


class StockList(generics.ListCreateAPIView):
    """
    get:
    Retourne la liste des stocks.
    post:
    Create and update store
    """
    permission_classes = (OnlyUserAndStaffPermission,)

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    filter_class = StockFilter
    ordering_fields = ('reference__ref', 'reference__name', 'reference__description', 'stock')

    def get_serializer_class(self):
        if self.request.method in ('POST', 'DELETE', 'PUT', 'PATCH'):
            serializer_class = StockCreateSerializer
        elif self.request.method in SAFE_METHODS:
            serializer_class = StockSerializer

        return serializer_class

    def get_queryset(self):
        return Stock.objects.filter(bar=self.kwargs['bar'])

    def create(self, validated_data, bar):
        dict_items = dict(self.request.data)

        # Vérification que le stock exite
        stocks = Stock.objects.filter(reference=int(dict_items.get("reference")[0]), bar=bar)

        if len(stocks) == 1:
            stocks[0].stock = int(dict_items.get("stock")[0])

            #Mise à jour des stocks en base de données
            stock_serializer = StockCreateSerializer(stocks[0], data={'stock': stocks[0].stock}, partial=True)
            if stock_serializer.is_valid():
                stock_serializer.save()
        else:
            #Enregistrement du stocks
            cust_req_data_orderitem = {
                'reference': int(dict_items.get("reference")[0]),
                'bar': bar,
                'stock': int(dict_items.get("stock")[0])
            }

            stock_serializer = StockCreateSerializer(data=cust_req_data_orderitem)
            if stock_serializer.is_valid():
                stock_serializer.save()

        return Response(stock_serializer.data)


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


class OrderDetail(generics.RetrieveAPIView, generics.CreateAPIView):
    """
    get:
    Retourne la commande correspondant à l'identifiant précisé.
    """
    queryset = Order.objects.all()

    permission_classes = (PostByClientAndGetByUserPermission,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            serializer_class = OrderCreateSerializer
        elif self.request.method == 'GET':
            serializer_class = OrderDetailSerializer

        return serializer_class

    def create(self, validated_data, pk):
        dict_items = dict(self.request.data)
        bar = pk

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
                cust_req_data_orderitem = {'reference': references[0].pk, 'order': order_serializer.data.get("pk")}

                # Vérification des stocks
                stocks = Stock.objects.filter(reference=references[0].pk, bar=bar)

                if len(stocks) == 1:
                    if stocks[0].stock > 0:
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
                        orderitem_serializer = OrderItemCreateSerializer(data=cust_req_data_orderitem)
                        if orderitem_serializer.is_valid():
                            orderitem_serializer.save()
                    else:
                        # La bière n'est plus en stock
                        lict_items.append({"ref": itemRef.get("ref"), "description": "La bière n'est plus disponible."})
                else:
                    # "La bière n'est pas disponible à ce comptoire
                    lict_items.append(
                        {"ref": itemRef.get("ref"), "description": "La bière n'est pas disponible à ce comptoir."})
            else:
                # La bière n'existe pas
                lict_items.append({"ref": itemRef.get("ref"), "description": "La référence demandée n'existe pas."})

        # Création de la response
        response = {"pk": order_serializer.data.get("pk")}
        response['items'] = lict_items

        return Response(response)


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
                         'description': 'Liste des comptoirs qui au moins une références épuisée.',
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


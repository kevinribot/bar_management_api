import django_filters.rest_framework
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.serializers import IntegerField

from .models import Reference, Bar, Stock, Order, OrderItem
from .serializers import ReferenceSerializer, BarSerializer, StockSerializer, MenuSerializer,  OrderSerializer, OrderCreateSerializer, OrderItemSerializer, RankSerializer
from django.db.models import Sum, Count


class ReferenceList(generics.ListCreateAPIView):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class BarList(generics.ListCreateAPIView):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer


class StockList(generics.ListAPIView):
    serializer_class = StockSerializer

    def get_queryset(self):
        return Stock.objects.filter(bar=self.kwargs['bar'])


class MenuList(generics.ListAPIView):
    queryset = Reference.objects.all()
    serializer_class = MenuSerializer

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
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderCreate(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer

    def create(self, validated_data, bar):
        dict_items = dict(self.request.data)
        cust_req_data_order = {'bar': bar}

        # Enregistrement de la commandes
        order_serializer = OrderSerializer(data=cust_req_data_order)
        if order_serializer.is_valid():
            order_serializer.save()

        response = {"pk": order_serializer.data.get("id")}

        lict_items = list()
        for itemRef in list(dict_items.get("items")):
            # Récupération de la référence
            references = Reference.objects.filter(ref=itemRef.get("ref"))
            if len(references) == 1:
                # La référence éxiste
                cust_req_data_orderitem = {'reference': references[0].pk, 'order': order_serializer.data.get("id")}

                # Vérification des stocks
                stocks = Stock.objects.filter(reference=references[0].pk, bar=bar)

                if len(stocks) == 1:
                    if stocks[0].stock > 0 :
                        # La bière est en stock - a faire la supression du stock
                        lict_items.append({"ref": references[0].ref,
                                           "name": references[0].name,
                                           "description": references[0].description})

                        stocks[0].stock = stocks[0].stock - 1

                        #Mise à jour des stocks en base de données
                        stock_serializer = StockSerializer(stocks[0], data={'stock': stocks[0].stock}, partial=True)
                        if stock_serializer.is_valid():
                            stock_serializer.save()

                        #Enregistrement des items de la commandes
                        orderitem_serializer = OrderItemSerializer(data=cust_req_data_orderitem)
                        if orderitem_serializer.is_valid():
                            orderitem_serializer.save()
                    else:
                        # La bière n'existe pas
                        lict_items.append({"ref": itemRef.get("ref"), "description": "La bière n'est plus disponible."})
                else:
                    # La bière n'existe pas
                    lict_items.append({"ref": itemRef.get("ref"), "description": "La bière n'est pas disponible à ce comptoire."})
            else:
                # La bière n'existe pas
                lict_items.append({"ref": itemRef.get("ref"), "description": "La référence demandée n'existe pas."})

        response['items'] = lict_items

        return Response(response)


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class RankList(generics.ListAPIView):
    serializer_class = RankSerializer

    def get_queryset(self):
        # Note the use of `get_queryset()` instead of `self.queryset`
        response = list()

        # Commentaire
        bars_all = Bar.objects.exclude(stocks__stock=0).distinct()
        response_all = {'name': 'all_stocks',
                        'description': 'Liste des comptoirs qui ont toutes les références en stock.',
                        'bars': (bar.pk for bar in bars_all)}

        # Commentaire
        bars_miss = Bar.objects.filter(stocks__stock=0).distinct()
        response_miss = {'name': 'miss_at_least_one',
                         'description': 'Liste des comptoirs qui au moins une références éppuisée.',
                         'bars': (bar.pk for bar in bars_miss)}

        # Commentaire
        bar_most = Bar.objects.annotate(total_order=Count('orders__orderItems')).order_by('-total_order').first()
        response_most = {'name': 'most_pints',
                         'description': 'Liste le comptoir avec le plus de pintes commandées.',
                         'bars': [bar_most.pk]}

        # Réponse
        response.append(response_all)
        response.append(response_miss)
        response.append(response_most)

        return response



class OrderItemList(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


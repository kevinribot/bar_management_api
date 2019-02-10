from rest_framework import serializers
from django.db.models import Sum

from .models import Reference, Bar, Stock, Order, OrderItem


class ReferenceSerializer(serializers.ModelSerializer):
    """
    Serializer of the model 'Reference'.
    """

    class Meta:
        model = Reference
        fields = ('ref', 'name', 'description')


class BarSerializer(serializers.ModelSerializer):
    """
    Serializer of the model 'Bar'.
    """

    class Meta:
        model = Bar
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer of the model 'Stock'.
    """

    reference = serializers.SlugRelatedField(slug_field="ref", write_only=True, queryset=Reference.objects.all())

    ref = serializers.CharField(source='reference.ref', read_only=True)
    name = serializers.CharField(source='reference.name', read_only=True)
    description = serializers.CharField(source='reference.description', read_only=True)

    class Meta:
        model = Stock
        fields = ('reference', 'ref', 'name', 'description', 'stock')


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer of the model 'Reference' allowing to know the state of the stock.
    """

    availability = serializers.SerializerMethodField()

    class Meta:
        model = Reference
        fields = ('ref', 'name', 'description', 'availability')

    # Allows to know if a reference is in stock.
    def get_availability(self, obj):
        if self.context.get("bar") > 0:
            return "available" if obj.stocks.get(bar=self.context.get("bar")).stock > 0 else "outofstock"

        return "available" if obj.stocks.aggregate(Sum("stock"))["stock__sum"] > 0 else "outofstock"


class RankSerializer(serializers.Serializer):
    """
    Serializer allowing to know information about bars.
    """

    name = serializers.CharField()
    description = serializers.CharField()
    bars = serializers.ListField()


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer of the model 'OrderItem'.
    """

    ref = serializers.CharField(source='reference.ref', read_only=True)
    name = serializers.CharField(source='reference.name', read_only=True)
    description = serializers.CharField(source='reference.description', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('ref', 'name', 'description', 'order', 'reference')
        extra_kwargs = {
            'order': {'write_only': True},
            'reference': {'write_only': True},
        }


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer of the model 'Order' without details of ordered references.
    """
    orderItems = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('pk', 'created', 'bar', 'orderItems')


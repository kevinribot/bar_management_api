from rest_framework import serializers
from .models import Reference, Bar, Stock, Order, OrderItem


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ('ref', 'name', 'description')


class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
        fields = ('pk', 'name')


class StockSerializer(serializers.ModelSerializer):
    ref = serializers.CharField(source='reference.ref', read_only=True)
    name = serializers.CharField(source='reference.name', read_only=True)
    description = serializers.CharField(source='reference.description', read_only=True)

    class Meta:
        model = Stock
        fields = ('ref', 'name', 'description', 'stock')


class MenuSerializer(serializers.ModelSerializer):
    availability = serializers.SerializerMethodField()

    class Meta:
        model = Reference
        fields = ('ref', 'name', 'description', 'availability')

    def get_availability(self, obj):
        if obj.total_stock > 0:
            return "available"
        else:
            return "outofstock"


class RankSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    bars = serializers.ListField(read_only=True)


class OrderCreateSerializer(serializers.Serializer):
    items = serializers.ListField()


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    ref = serializers.CharField(source='reference.ref', read_only=True)
    name = serializers.CharField(source='reference.name', read_only=True)
    description = serializers.CharField(source='reference.description', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('ref', 'name', 'description')


class OrderDetailSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('pk', 'created', 'bar', 'orderItems')

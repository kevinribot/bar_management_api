from rest_framework import serializers

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


class StockCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to create a model object 'Stock'.
    """

    class Meta:
        model = Stock
        fields = ('reference', 'stock', 'bar')


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer of the model 'Stock'.
    """

    ref = serializers.CharField(source='reference.ref', read_only=True)
    name = serializers.CharField(source='reference.name', read_only=True)
    description = serializers.CharField(source='reference.description', read_only=True)

    class Meta:
        model = Stock
        fields = ('ref', 'name', 'description', 'stock')


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
        if obj.total_stock > 0:
            return "available"
        else:
            return "outofstock"


class RankSerializer(serializers.Serializer):
    """
    Serializer allowing to know information about bars.
    """

    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    bars = serializers.ListField(read_only=True)


class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer to create an object 'Order'.
    """

    items = serializers.ListField()


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to create a model object 'OrderItem'.
    """

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer of the model 'Order' without details of ordered references.
    """

    class Meta:
        model = Order
        fields = ('pk', 'bar')


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer of the model 'OrderItem'.
    """

    ref = serializers.CharField(source='reference.ref', read_only=True)
    name = serializers.CharField(source='reference.name', read_only=True)
    description = serializers.CharField(source='reference.description', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('ref', 'name', 'description')


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer of the model 'Order' with details of ordered references.
    """

    orderItems = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('pk', 'created', 'bar', 'orderItems')


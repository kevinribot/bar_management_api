from django.db import models


class Reference(models.Model):
    """
    Model of data - Reference
    """

    ref = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)

    def __str__(self):
        return str(self.ref)

    class Meta:
        unique_together = ('ref', )


class Bar(models.Model):
    """
    Model of data - Bar
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Stock(models.Model):
    """
    Model of data - Stock
    Allows you to manage the reference quantity available at a bar.
    """

    stock = models.IntegerField()
    reference = models.ForeignKey(Reference, related_name='stocks', on_delete=models.CASCADE)
    bar = models.ForeignKey(Bar, related_name='stocks', on_delete=models.CASCADE)

    def __str__(self):
        return self.bar.name + " - " + self.reference.ref + " (" + str(self.stock) + ")"

    class Meta:
        unique_together = ('bar', 'reference')


# Model of data - Order.
class Order(models.Model):
    """
    Model of data - Order
    Associate an order with a bar.
    """

    bar = models.ForeignKey(Bar, related_name='orders', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class OrderItem(models.Model):
    """
    Model of data - OrderItem
    Represents the list of references ordered in an order.
    """

    order = models.ForeignKey(Order, related_name='orderItems', on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, related_name='orderItems', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


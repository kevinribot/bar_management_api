from django.db import models


# Model of data - Reference.
class Reference(models.Model):
    ref = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)

    def __str__(self):
        return str(self.pk)


# Model of data - Bar.
class Bar(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.pk)


# Model of data - Stock.
class Stock(models.Model):
    stock = models.IntegerField()
    reference = models.ForeignKey(Reference, related_name='stocks', on_delete=models.CASCADE)
    bar = models.ForeignKey(Bar, related_name='stocks', on_delete=models.CASCADE)

    def __str__(self):
        return self.bar.name + " - " + self.reference.ref + " (" + self.stock + ")"


# Model of data - Order.
class Order(models.Model):
    bar = models.ForeignKey(Bar, related_name='orders', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


# Model of data - OrderItem.
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderItems', on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, related_name='orderItems', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


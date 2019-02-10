from django.dispatch import receiver
from django.db.models.signals import post_save

from bars.models import Stock, OrderItem


@receiver(post_save, sender=OrderItem)
def my_callback(sender, **kwargs):
    """
    Verification of stock quantity during an update.
    An alert is sent when less than 2 references remain in stock.
    """
    orderItem = kwargs['instance']
    # Update of stocks to database
    stock = Stock.objects.filter(reference=orderItem.reference.pk, bar=orderItem.order.bar.pk).first()
    stock.stock = stock.stock - 1
    Stock.objects.filter(reference=orderItem.reference.pk, bar=orderItem.order.bar.pk).update(stock=stock.stock)

    if 0 < stock.stock <= 2:
        print(
            "La référence '{0}' n'est bientôt plus disponible (Quantité restante : {1})".format(stock.reference.ref,
                                                                                                stock.stock))
    elif stock.stock == 0:
        print("La référence '{0}' n'est plus disponible.".format(stock.reference.ref, ))


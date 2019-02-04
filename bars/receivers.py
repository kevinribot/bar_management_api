from django.dispatch import receiver
from django.db.models.signals import post_save

from bars.models import Stock


@receiver(post_save)
def my_callback(sender, **kwargs):
    """
    Verification of stock quantity during an update.
    An alert is sent when less than 2 references remain in stock.
    """

    if issubclass(sender, Stock):
        stock = kwargs['instance']
        if 0 < stock.stock <= 2:
            print(
                "La référence '{0}' n'est bientôt plus disponible (Quantité restante : {1})".format(stock.reference.ref,
                                                                                                    stock.stock))
        elif stock.stock == 0:
            print("La référence '{0}' n'est plus disponible.".format(stock.reference.ref, ))

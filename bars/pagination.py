from rest_framework.pagination import PageNumberPagination


# Creation d'une pagination personalisee qui permet à l'utlisateur de choisir le nombre d'item qu'il veut afficher
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


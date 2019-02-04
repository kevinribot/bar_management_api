from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Creation of a personalized pagination.
    The 'page_size' parameter allows the user to choose the number of items on a page (default: 10, max: 100).
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


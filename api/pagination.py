from rest_framework import pagination
from rest_framework.response import Response

class LivrePagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5
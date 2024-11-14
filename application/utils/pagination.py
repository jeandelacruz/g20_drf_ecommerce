from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'per_page'
    max_page_size = 50
    default_page = 1
    default_page_size = 10

    def get_page_number(self, request, paginator):
        page = request.query_params.get(
            self.page_query_param, self.default_page
        )
        return int(page)

    def get_page_size(self, request):
        per_page = request.query_params.get(
            self.page_size_query_param, self.default_page_size
        )
        self.page_size = int(per_page)
        return self.page_size

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'pagination': {
                'totalRecords': self.page.paginator.count,
                'totalPages': self.page.paginator.num_pages,
                'perPage': self.page_size,
                'currentPage': self.page.number
            }
        })

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CommentPagination(PageNumberPagination):
    """
    Custom pagination class for comments.
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
    last_page_strings = ("last",)

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "results": data,
            }
        )

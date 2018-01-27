from collections import OrderedDict
from urllib.parse import urlparse, parse_qs

from rest_framework.pagination import CursorPagination
from rest_framework.response import Response



class CustomCursorPagination(CursorPagination):
    def get_paginated_response(self, data):
        next_link = self.get_next_link()
        previous_link = self.get_previous_link()

        # Retrieves next / previous cursor from next / previous links
        next_cursor = parse_qs(urlparse(next_link).query)['cursor'][0] if next_link else None
        previous_cursor = parse_qs(urlparse(previous_link).query)['cursor'][0] if previous_link else None

        return Response(OrderedDict([
            ('next_cursor', next_cursor),
            ('previous_cursor', previous_cursor),
            ('results', data)
        ]))

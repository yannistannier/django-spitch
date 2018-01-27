from apps.core.api.pagination import CustomCursorPagination


class AskListPagination(CustomCursorPagination):
    page_size = 10


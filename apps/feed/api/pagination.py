from apps.core.api.pagination import CustomCursorPagination


class FeedListPagination(CustomCursorPagination):
    page_size = 5


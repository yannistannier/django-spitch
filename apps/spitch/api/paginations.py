from apps.core.api.pagination import CustomCursorPagination


class SpitchSwipePagination(CustomCursorPagination):
    page_size = 10
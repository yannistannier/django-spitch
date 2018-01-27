from apps.core.api.pagination import CustomCursorPagination


class SpitchPagination(CustomCursorPagination):
    page_size = 8


class SearchUserPagination(CustomCursorPagination):
    page_size = 10
    ordering = '-date_joined'

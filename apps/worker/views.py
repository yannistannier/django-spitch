import importlib

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class WorkerApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        datas = request.data
        if "path" and "method" in datas:
            module = importlib.import_module(datas["path"])
            method = getattr(module, datas["method"], None)

            args = datas["args"] if "args" in datas else ()
            kwargs = datas["kwargs"] if "kwargs" in datas else {}

            if method:
                method(*args, **kwargs)

        return Response(status=status.HTTP_200_OK)

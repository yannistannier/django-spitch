import inspect
import boto3
import json
from functools import wraps

from django.conf import settings


class shared_task(object):

    def __init__(self, view_func):
        self.view_func = view_func
        wraps(view_func)(self)

    def __call__(self, *args, **kwargs):
        return self.view_func(*args, **kwargs)

    def delay(self, *args, **kwargs):
        method = self.view_func.__name__
        path = inspect.getmodule(self.view_func).__name__
        self.message = {
            'method': method,
            'path': path,
            'args': args,
            'kwargs': kwargs
        }
        self.send_message()

    def send_message(self):
        client = boto3.client('sqs')
        client.send_message(
            QueueUrl=settings.SQS_WORKER,
            MessageBody=json.dumps(self.message)
        )



# {
# 	"method": "test",
# 	"kwargs": {},
# 	"args": [],
# 	"path": "apps.worker.tasks"
# }


# Free notification structure example
# {
#   "fcm": {
#     "S": "fcmstring"
#   },
#   "body": {
#     "S": "body"
#   },
#   "title": {
#     "S": "title"
#   },
#   "type": {
#     "N": "0"
#   },
#   "obj": {
#     "M": {
#       "id": {
#         "N": "152"
#       },
#       "spitch": {
#         "N": "1069"
#       },
#       "spitch_transcoded": {
#         "S": "https://spitchdev-bucket-xxxxx.s3.amazonaws.com/media/287/spitch/1069/xxxxx.mp4"
#       },
#       "text": {
#         "S": "Avez vous deja vu une grosse araignée ?"
#       }
#     }
#   },
#   "user": {
#     "M": {
#       "first_name": {
#         "S": "Antoine"
#       },
#       "id": {
#         "N": "287"
#       },
#       "last_name": {
#         "S": "Boudic"
#       },
#       "photo": {
#         "S": "https://spitchdev-bucket-xxxxx.s3.amazonaws.com/media/287/photo/xxxxxxx.jpg"
#       },
#       "username": {
#         "S": "AntoineBoudic"
#       }
#     }
#   }
# }
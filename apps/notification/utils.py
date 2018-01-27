import boto3
import time

from apps.authentication.models import User
from apps.ask.models import Ask
from apps.spitch.models import Spitch
from django.conf import settings


class NotificationHandler(object):
    # 1 -> follow / 2 -> like / 3 -> ask all / 4 -> ask private / 5 -> video answer all / 6 -> video answer private
    def __init__(self, emitter, type_name, object=None):
        self.type_name = type_name
        self.object = object
        self.emitter = emitter
        self.init_dynamodb()

    def perform_follow_user(self):
        self.receiver = self.object
        self.send_notification(1)

    def perform_follow_all(self):
        self.receivers = User.objects.filter(id__in=self.object)
        self.send_notifications(1)

    def perform_ask(self):
        if self.object.is_private():
            self.receivers = self.object.receivers.all()
            print(self.receivers)
            self.send_notifications(4)
        else:
            self.get_followers()
            self.send_notifications(3)

    def perform_new_spitch(self):
        if self.object.ask.is_private():
            self.receiver = self.object.ask.user
            self.send_notification(6)
        else:
            self.get_followers()
            self.send_notifications(5)

    def perform_like_spitch(self):
        self.receiver = self.object.user
        self.send_notification(2)


    def send_notifications(self, type):
        with self.table.batch_writer() as batch:
            for receiver in self.receivers:
                batch.put_item(
                    Item=self.get_item(receiver, type)
                )

    def send_notification(self, type):
        self.table.put_item(
            Item=self.get_item(self.receiver, type)
        )


    def get_item(self, receiver, type):
        item = {
            'id': str(receiver.id),
            'uid': self.get_uuid(type),
            'user': self.transform_instance_to_dict(self.emitter),
            'type': type,
            'timestamp': int(time.time()),
            'fcm': self.get_fcm(receiver),
            'lang': receiver.country,
            'vue' : 0
        }
        if type in  (2, 3, 4, 5, 6):
            item['obj'] = self.transform_instance_to_dict(self.object)

        return item

    def get_followers(self):
        self.receivers = User.objects.filter(follows__follow=self.emitter)


    def get_uuid(self, type):
        if type == 1:
            return str(self.emitter.id)+"f"
        if type == 2:
            return str(self.object.id)+"-"+str(self.emitter.id)+"-l"
        if type in (3, 4):
            return str(self.object.id)+"q"
        if type in (5, 6):
            return str(self.object.id)+"s"
        return ""

    def get_fcm(self, user):
        #condition if allow notification, so return fcm else return None
        return user.fcm if user.fcm else False

    def transform_instance_to_dict(self, instance):
        if isinstance(instance, User):
            return {
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "id": instance.id,
                "username": instance.username,
                "photo": str(instance.photo.url)
            }
        if isinstance(instance, Ask):
            return {
                "text": instance.text,
                "id": instance.id
            }
        if isinstance(instance, Spitch):
            return {
                "text": instance.ask.text,
                "id": instance.ask.id,
                "spitch": instance.id,
                "spitch_transcoded" : instance.spitch_transcoded.url
            }

        return {}

    def init_dynamodb(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(settings.DYNAMODB_TABLE)

    def send(self):
        method_name = 'perform_{}'.format(self.type_name).lower()
        method = getattr(self, method_name, None)
        if method:
            method()

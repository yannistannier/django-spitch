import datetime
import time
from elasticsearch import Elasticsearch, RequestsHttpConnection

from django.conf import settings


class SyncElasticSearch(object):
    host = settings.NAME_ES_DOMAIN
    index = None
    doc_type = None

    def __init__(self, id):
        self.id = id
        if "https" in self.host:
            self.es = Elasticsearch(
                [self.host],
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection
            )
        else:
            self.es = Elasticsearch([self.host])


    def transform_user_to_dict(self, instance):
        return {
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "id": instance.id,
            "username": instance.username,
            "photo": str(instance.photo.url)
        }

    def create(self):
        self.es.index(index=self.index, doc_type=self.doc_type, id=int(self.id), body=self.object)

    def delete(self):
        if self.es.exists(index=self.index, doc_type=self.doc_type, id=int(self.id)):
            self.es.delete(index=self.index, doc_type=self.doc_type, id=int(self.id))

    def update(self):
        if self.es.exists(index=self.index, doc_type=self.doc_type, id=int(self.id)):
            self.es.update(index=self.index, doc_type=self.doc_type, id=int(self.id), body={"doc": self.object})



class SyncAsk(SyncElasticSearch):
    index = "questions"
    doc_type = "question"

    def set_object(self, object):
        self.object = {
            "text" : object.text,
            "tags" : list(object.tags.values_list("tag", flat=True)),
            "lang" : object.user.lang,
            "user" : self.transform_user_to_dict(object.user),
            "date": datetime.date.today(),
            "timestamp": int(time.time())
        }
        return self


class SyncUser(SyncElasticSearch):
    index = "users"
    doc_type = "user"

    def set_object(self, object):
        self.object = self.transform_user_to_dict(object)
        self.object["lang"] = object.lang
        self.object["country"] = object.country
        return self

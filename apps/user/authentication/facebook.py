# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import facebook


class Facebook():
    graph = None

    def __init__(self, token):
        self.graph = facebook.GraphAPI(access_token=token, version='2.9')


    def get_id(self):
        event = self.graph.get_object(id='me')
        return event['id']


    def get_profile(self, username):
        event = self.graph.get_object(id='me', fields='id,first_name,last_name,email,picture.type(large)')
        obj = {
            "username": username,
            "type": "facebook",
            "email": event['email'],
            "first_name": event['first_name'],
            "last_name": event['last_name'],
            "idsn": event['id'],
            "photo": event['picture']['data']['url']
        }
        return obj


    def get_friends(self):
        event = self.graph.get_all_connections(id='me', connection_name='friends')
        return [x['id'] for x in event]

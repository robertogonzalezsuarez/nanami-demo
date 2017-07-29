# -*- coding: utf-8 -*-
import urllib
import json

import logging

from google.appengine.api import urlfetch

from environment.environment import DATABASE_REF


class Firebase():

    root_url = DATABASE_REF

    # The methods set, push, update and remove are intended to mimic Firebase
    # API calls.
    @staticmethod
    def request(method, query_url, auth_token, **kwargs):
        if 'payload' in kwargs:
            kwargs['payload'] = json.dumps(kwargs['payload'])

        params = {}
        if 'params' in kwargs:
            params.update(kwargs['params'])
            del kwargs['params']
        headers = {}
        if auth_token:
            headers.update({'Authorization': 'Bearer ' + auth_token})

        # Do we need to chuck on some extra params?
        if params:
            url = '%s?%s' % (Firebase.root_url + query_url + '.json', urllib.urlencode(params))
        else:
            url = Firebase.root_url + query_url + '.json'

        response = urlfetch.fetch(url, method=method, headers=headers, **kwargs)
        return json.loads(response.content)

    @staticmethod
    def get(url, auth_token=None, **kwargs):
        return Firebase.request(urlfetch.GET, url, auth_token, params=kwargs)

    @staticmethod
    def post(url, payload, auth_token=None):
        return Firebase.request(urlfetch.POST, url, auth_token, payload=payload)

    @staticmethod
    def put(url, payload, auth_token=None):
        return Firebase.request(urlfetch.PUT, url, auth_token, payload=payload)

    @staticmethod
    def patch(url, payload, auth_token=None):
        return Firebase.request(urlfetch.PATCH, url, auth_token, payload=payload)

    @staticmethod
    def delete(url, auth_token=None):
        return Firebase.request(urlfetch.DELETE, url, auth_token)

# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class Profile(ndb.Model):
    name = ndb.StringProperty(indexed=True)


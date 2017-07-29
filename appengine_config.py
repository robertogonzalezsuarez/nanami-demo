# -*- coding: utf-8 -*-
from google.appengine.ext import vendor
import os.path

__author__ = 'nanami'

vendor.add('lib')


def patched_expanduser(path):
    return path

os.path.expanduser = patched_expanduser

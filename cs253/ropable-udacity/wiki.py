from google.appengine.ext import db
from google.appengine.api import memcache
from main import Handler


class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    cookie = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)


class WikiPage(db.Model):
    name = db.StringProperty(required=True)
    user = db.ReferenceProperty(User)
    content = db.TextProperty(required=True)
    modified = db.DateTimeProperty(auto_now=True)


class WikiHistory(db.Model):
    page = db.ReferenceProperty(WikiPage)
    user = db.ReferenceProperty(User)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

import logging
import datetime
import os
import webapp2
import jinja2
import re
import hmac
import cgi
import json
import time
from google.appengine.ext import db

import asciichan
import blog

SALT = 'mmmsaltysalt'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
    autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        self.render('front.html')


app = webapp2.WSGIApplication([('/', MainPage)] + blog.URLS + asciichan.URLS, debug=True)

#!/usr/bin/env python
import webapp2

form = '''
<!DOCTYPE html>
<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>
  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"></textarea>
      </br>
      <input type="submit">
    </form>
  </body>
</html>
'''

import cgi, string

def rot13_html(text=None):
    if not text: return None
    rot13 = string.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
    text = string.translate(text, rot13)
    return cgi.escape(text)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(form)

class TestHandler(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(self.request)
        #q = self.request.get('q')
        #self.response.out.write(q)

app = webapp2.WSGIApplication([('/', MainHandler),('/testform', TestHandler)],
    debug=True)

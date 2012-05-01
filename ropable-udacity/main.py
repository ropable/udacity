#!/usr/bin/env python
import webapp2

form = '''
<form method="post">
    What is your birthday?
    <input name="q">
    <input type="submit">
</form>
'''
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

#!/usr/bin/env python
import webapp2
import cgi
import string
import re

def rot13_text(text=None):
    if not text: return None
    rot13 = string.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
    text = string.translate(text.encode('ascii'), rot13)
    return cgi.escape(text)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write("Hello, Udacity!")

# UNIT 2 Homework
base_page = '''
<!DOCTYPE html>
<html>
    <head>
        <title>{title}</title>
        <link type=""text/css rel="stylesheet" href="/css/bootstrap.min.css">
    </head>
    <body>
        {body}
    </body>
</html>
'''

rot13_form = '''<h1>Enter some text to ROT13:</h1>
<form method="post">
    <textarea name="text">{0}</textarea>
    </br>
    <input type="submit">
</form>'''

class Rot13Handler(webapp2.RequestHandler):
    def write_form(self, form_text=''):
        form = rot13_form.format(form_text)
        page = base_page.format(title='Unit 2 HW 1: ROT13', body=form)
        self.response.out.write(page)

    def get(self):
        self.write_form()

    def post(self):
        text = self.request.get('text')
        form_text = (rot13_text(text))
        self.write_form(form_text)

signup_form = '''<h1>Signup:</h1>
<form method="post">
    <label for="username">Username*</label>
    <input type ="text" name="username" value="{username}">
    <span class="help-inline">{username_error}</span>
    <br>
    <label for="password">Password*</label>
    <input type ="password" name="password" value="">
    <span class="help-inline">{password_error}</span>
    <br>
    <label for="verify">Verify password*</label>
    <input type ="password" name="verify" value=""><br>
    <label for="email">Email</label>
    <input type ="email" name="email" value="{email}">
    <span class="help-inline">{email_error}</span><br>
    </br>
    <input type="submit">
</form>'''
class UserSignupHandler(webapp2.RequestHandler):
    def write_form(self, username='', username_error='', password_error='', email='', email_error=''):
        form = signup_form.format(username=username, username_error=username_error,
            password_error=password_error, email=email, email_error=email_error)
        page = base_page.format(title='Unit 2 HW 2: User signup', body=form)
        self.response.out.write(page)

    def get(self):
        self.write_form()
        
    def post(self):
        errors = False
        username = self.request.get('username')
        
        if username == '':
            username_error = 'You must choose a username.'
            errors = True
        elif not re.match('^[a-zA-Z0-9_-]{3,20}$', username):
            username_error = "That's not a valid username."
            errors = True
        else:
            username_error = ''
        password = self.request.get('password')
        verify = self.request.get('verify')
        if password != verify:
            password_error = 'The passwords did not match.'
            errors = True
        elif not re.match("^.{3,20}$", password):
            password_error = 'That password is not valid.'
            errors = True
        elif not password:
            password_error = 'You must choose a password.'
            errors = True
        else:
            password_error = ''
        email = self.request.get('email')
        email_error = ''
        if email:
            if not re.match("^[\S]+@[\S]+\.[\S]+$", email):
                email_error = 'That email is not valid.'
                errors = True
        if errors:
            self.write_form(username=username, username_error=username_error,
                password_error=password_error, email=email, email_error=email_error)
        else:
            # No validation errors
            self.redirect('/unit2/welcome?username={0}'.format(username))

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write('<h1>Welcome, {0}!'.format(username))

app = webapp2.WSGIApplication([('/', MainHandler),
    ('/unit2/rot13', Rot13Handler),
    ('/unit2/signup', UserSignupHandler),
    ('/unit2/welcome', WelcomeHandler),
    ], debug=True)
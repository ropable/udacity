import re
import asciichan
import hmac
import cgi
from google.appengine.ext import db

SALT = 'mmmsaltysalt'

class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    cookie = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)


class UserSignup(asciichan.Handler):
    def render_form(self, username='', username_error='', password_error='', email='', email_error=''):
        self.render('signup-form.html',  username=username, username_error=username_error,
            password_error=password_error, email=email, email_error=email_error)

    def get(self):
        self.render_form()

    def post(self):
        errors = False
        username = self.request.get('username')
        # Form validation
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
            password_error = 'That password is not valid, or too short.'
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
        # Test that username does not already exist:
        if username:
            u = db.GqlQuery("SELECT * FROM User WHERE username='{0}'".format(username)).get()
            if u: # Got a result.
                username_error = "That username is already taken."
                errors = True
        if errors:
            self.render_form(username=username, username_error=username_error,
                password_error=password_error, email=email, email_error=email_error)
        else:
            # No validation errors: create a user, add a cookie, and redirect to the welcome page
            hashed_pw = hmac.new(SALT, username+password).hexdigest()
            user = User(username=username, password=hashed_pw)
            user.put()
            # Save the user's cookie.
            cookie = '{0}|{1}'.format(user.key().id(), hmac.new(SALT, username).hexdigest())
            user.cookie = cookie
            user.put()
            self.response.headers.add_header('Set-Cookie', 'user_id={0}; Path=/'.format(cookie))
            self.redirect('/wiki/welcome')


class UserLogin(asciichan.Handler):
    def get(self):
        cookie = self.request.cookies.get('user_id')
        if cookie:
            user = db.GqlQuery("SELECT * FROM User WHERE cookie='{0}'".format(cookie)).get()
            if user:
                self.redirect('/wiki')
        self.render('login-form.html')

    def post(self):
        logged_in = False
        username = self.request.get('username')
        password = self.request.get('password')
        if username and password:
            hashed_pw = hmac.new(SALT, username+password).hexdigest()
            user = db.GqlQuery("SELECT * FROM User WHERE password='{0}'".format(hashed_pw)).get()
            if user:
                logged_in = True
                cookie = '{0}|{1}'.format(user.key().id(), hmac.new(SALT, username).hexdigest())
                self.response.headers.add_header('Set-Cookie', 'user_id={0}; Path=/'.format(cookie))
        if logged_in:
            self.redirect('/wiki')
        else:
            self.render('login-form.html', login_error='Invalid login')


class WelcomeUser(asciichan.Handler):
    def get(self):
        cookie = self.request.cookies.get('user_id')
        if cookie:
            # Get the user whose cookie this is.
            user = db.GqlQuery("SELECT * FROM User WHERE cookie='{0}'".format(cookie)).get()
            if user:
                self.render('welcome.html', username=escape_text(user.username))
            else:
                self.redirect('/wiki/signup')
        else:
            self.redirect('/wiki/signup')


class UserLogout(asciichan.Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.redirect('/wiki/signup')


def escape_text(s):
    return cgi.escape(s, quote=True)
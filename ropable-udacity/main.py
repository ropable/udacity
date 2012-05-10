import os
import webapp2
import jinja2
import re
import hmac
import cgi
from google.appengine.ext import db

SALT = 'mmmsaltysalt'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
    autoescape=True)

def escape_text(s):
    return cgi.escape(s, quote=True)

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
        
class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class AsciiPage(Handler):
    def render_front(self, title='', art='', error=''):
        arts = db.GqlQuery('SELECT * FROM Art ORDER BY created DESC')
        self.render('ascii.html', title=title, art=art, error=error, arts=arts)

    def get(self):
        self.render_front()
        
    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')
        
        if title and art:
            a = Art(title=title, art=art)
            a.put()
            self.redirect('/')
        else:
            error = "Please input both a title and some art!"
            self.render_front(title, art, error)

class BlogEntry(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    
class BlogPage(Handler):
    def get(self, entry=None):
        if not entry:
            e = db.GqlQuery('SELECT * from BlogEntry ORDER BY created DESC LIMIT 10')
            self.render('blog.html', latest_entries=e)
        else:
            e = BlogEntry.get_by_id(ids=int(entry))
            self.render('blog.html', single_entry=e)
            
class NewBlogPost(Handler):
    def get(self):
        self.render('new_entry_form.html')
        
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        if subject and content:
            entry = BlogEntry(subject=subject, content=content)
            entry.put()
            self.redirect('/unit3/blog/{0}'.format(entry.key().id()))
        else:
            error = "New blog post requires both a subject and a title."
            self.render('new_entry_form.html', subject=subject, content=content, error=error)

class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    cookie = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    
class WelcomeUser(Handler):
    def get(self):
        cookie = self.request.cookies.get('user_id')
        if cookie:
            # Get the user whose cookie this is.
            user = db.GqlQuery("SELECT * FROM User WHERE cookie='{0}'".format(cookie)).get()
            if user:
                self.render('welcome.html', username=escape_text(user.username))
            else:
                self.redirect('/unit4/signup')
        else:
            self.redirect('/unit4/signup')

class UserSignup(Handler):
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
            self.redirect('/unit4/welcome')

class UserLogin(Handler):
    def get(self):
        cookie = self.request.cookies.get('user_id')
        if cookie:
            user = db.GqlQuery("SELECT * FROM User WHERE cookie='{0}'".format(cookie)).get()
            if user:
                self.redirect('/unit4/welcome')
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
                self.response.headers.add_header('Set-Cookie', 'user_id={0}; Path=/'.format(cookie))
        if logged_in:
            self.redirect('/unit4/welcome')
        else:
            self.render('login-form.html', login_error='Invalid login')

class UserLogout(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.redirect('/unit4/signup')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/unit3/ascii', AsciiPage),
    ('/unit3/blog', BlogPage),
    ('/unit3/blog/newpost', NewBlogPost),
    ('/unit3/blog/([^/]+)', BlogPage),
    ('/unit4/signup', UserSignup),
    ('/unit4/login', UserLogin),
    ('/unit4/logout', UserLogout),
    ('/unit4/welcome', WelcomeUser),
], debug=True)
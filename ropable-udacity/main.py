import os
import webapp2
import jinja2
from google.appengine.ext import db

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
    
class UserSignup(Handler):
    #def write_form(self, username='', username_error='', password_error='', email='', email_error=''):
    #    form = signup_form.format(username=username, username_error=username_error,
    #        password_error=password_error, email=email, email_error=email_error)
    #    page = base_page.format(title='Unit 2 HW 2: User signup', body=form)
    #    self.response.out.write(page)
    #def render_front(self, title='', art='', error=''):
    #    arts = db.GqlQuery('SELECT * FROM Art ORDER BY created DESC')
    #    self.render('ascii.html', title=title, art=art, error=error, arts=arts)
    def render_form(self, username='', username_error='', password_error='', email='', email_error=''):
        self.render('signup-form.html',  username_error=username_error, 
            password_error=password_error, email=email, email_error=email_error)

    def get(self):
        self.render_form()
        
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

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/unit3/ascii', AsciiPage),
    ('/unit3/blog', BlogPage),
    ('/unit3/blog/newpost', NewBlogPost),
    ('/unit3/blog/([^/]+)', BlogPage),
    ('/unit4/signup', UserSignup),
], debug=True)
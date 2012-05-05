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
            self.render('blog.html')
        else:
            self.response.write(entry)
            
class NewBlogPost(Handler):
    pass
    
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/unit3/ascii', AsciiPage),
    ('/unit3/blog', BlogPage),
    ('/unit3/blog/newpost', NewBlogPost),
    ('/unit3/blog/([^/]+)', BlogPage),
], debug=True)
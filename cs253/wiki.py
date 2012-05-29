import re
import asciichan
import auth
from google.appengine.ext import db
from google.appengine.api import memcache


class Wiki(db.Model):
    name = db.StringProperty(required=True)
    user = db.ReferenceProperty(auth.User, required=True)
    content = db.TextProperty(required=True)
    modified = db.DateTimeProperty(auto_now=True)


class WikiHistory(db.Model):
    page = db.ReferenceProperty(Wiki, required=True)
    user = db.ReferenceProperty(auth.User, required=True)
    version = db.IntegerProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class WikiFrontPage(asciichan.Handler):
    def get(self):
        self.redirect('/wiki/')
        
        
class WikiPage(asciichan.Handler):
    def get(self, page_name):
        user = get_user(self.request)
        version = self.request.get('v')
        # Try to get this page from the cache.
        page = page_content(page_name)
        #print(page)
        if user and not page:
            self.redirect('/wiki/_edit{0}'.format(page_name))
        if page and version:
            # Serve up the relevant page version.
            history = page_history(page, version)
            self.render('wiki.html', user=user, page=page, content=history.content)
        if page:
            self.render('wiki.html', user=user, page=page, content=page.content)
        else:
            self.redirect('/wiki/_edit{0}'.format(page_name))
        # Page doesn't exist yet? Redirect to the edit page.
        

class EditPage(asciichan.Handler):
    def get(self, page_name):
        user = get_user(self.request)
        # Get any existing page content from the cache.
        page = page_content(page_name)
        self.render('edit_wiki.html', user=user, page=page)

    def post(self, page_name):
        content = self.request.get('content')
        page = page_content(page_name)
        user = get_user(self.request)
        if content and page:
            if content == page.content: # Save needless versions being created.
                self.redirect('/wiki{0}'.format(page_name))
            else:
                # Edit an existing page.
                page.content = content
                page.put()
                history = list(db.GqlQuery("SELECT * FROM WikiHistory WHERE page=:1", page.key()))[0]
                new_history = WikiHistory(page=page, user=user, version=history.version+1, content=content)
                new_history.put()
                page = page_content(page_name, update=True)
                self.redirect('/wiki{0}'.format(page_name))
        elif content and not page:
            # Create a new page, plus history.
            page = Wiki(name=page_name, user=user, content=content)
            page.put()
            history = WikiHistory(page=page, user=user, version=1, content=content)
            history.put()
            self.redirect('/wiki{0}'.format(page_name))
        else:
            error = 'Please input some content!'
            self.render('edit_wiki.html', name=page_name, error=error)

class PageHistory(asciichan.Handler):
    def get(self, page_name):
        user = get_user(self.request)
        page = page_content(page_name)
        if page:
            history = db.GqlQuery("SELECT * FROM WikiHistory WHERE page=:1 ORDER BY created DESC", page.key())
            history = list(history)
            self.render('wiki_history.html', user=user, page=page, history=history)
        if user and not page:
            self.redirect('/wiki/_edit{0}'.format(page_name))
            
        
def page_content(page_name, update=False):
    page = memcache.get(page_name)
    if page is None or update:
        page = db.GqlQuery("SELECT * FROM Wiki WHERE name='{0}'".format(page_name)).get()
        if page:
            memcache.set(page_name, page)
    return page
    
def page_history(page, version):
    history = memcache.get('{0}|v{1}'.format(page.name, version))
    if history is None:
        history = db.GqlQuery("SELECT * FROM WikiHistory WHERE page=:1 AND version={0}".format(version), page.key()).get()
        memcache.set('{0}|v{1}'.format(page.name, version), history)
    return history

def get_user(request):
    cookie = request.cookies.get('user_id')
    if cookie:
        user = db.GqlQuery("SELECT * FROM User WHERE cookie='{0}'".format(cookie)).get()
    else:
        user = None
    return user

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
URLS = [
    ('/wiki', WikiFrontPage),
    ('/wiki/signup', auth.UserSignup),
    #('/wiki/welcome', auth.WelcomeUser),
    ('/wiki/login', auth.UserLogin),
    ('/wiki/logout', auth.UserLogout),
    ('/wiki/_edit' + PAGE_RE, EditPage),
    ('/wiki/_history' + PAGE_RE, PageHistory),
    ('/wiki' + PAGE_RE, WikiPage),
    ]

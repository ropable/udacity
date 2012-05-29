import re
import asciichan
import auth
import logging
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


class WikiPage(asciichan.Handler):
    def get(self, page_name=None):
        user = get_user(self.request)
        # Assume a 'blank' page name means 'front' (also handle trailing forward slash).
        if not page_name or page_name == '/':
            page_name = 'front'
        else:
            page_name = page_name[1:]
        # Try to get this page from the cache.
        page = page_content(page_name)
        version = self.request.get('v')
        if user and not page:
            self.redirect('/wiki/_edit/{0}'.format(page_name))
        elif page and version:
            # Serve up the relevant page version.
            history = page_history(page, version)
            self.render('wiki.html', user=user, page=page, content=history.content)
        elif page and not version:
            if user:
                logging.info('User {0} opened wiki page {1} | {2}'.format(user.username, page_name, str(self.request)))
            else:
                logging.info('Anon user opened wiki page {0} | {1}'.format(page_name, str(self.request)))
            self.render('wiki.html', user=user, page=page, content=page.content)
        else:
            # Render a "Does not exit" placeholder for anon users.
            self.render('wiki_blank.html', name=page_name)
    
class EditPage(asciichan.Handler):
    def get(self, page_name=None):
        user = get_user(self.request)
        # Assume a 'blank' page name means 'front' (also handle trailing forward slash).
        if not page_name or page_name == '/':
            page_name = 'front'
        else:
            page_name = page_name[1:]
        # Get any existing page content from the cache.
        page = page_content(page_name)
        version = self.request.get('v')
        if not user:
            # Anon users can't edit.
            self.redirect('/wiki/login')
        elif user and page and version:
            # User wants to use an older version.
            history = page_history(page, version)
            self.render('edit_wiki.html', user=user, page=page, content=history.content)
        else:
            # User logged in - edit as normal.
            self.render('edit_wiki.html', user=user, page=page)

    def post(self, page_name):
        content = self.request.get('content')
        page_name = page_name[1:]
        page = page_content(page_name)
        user = get_user(self.request)
        if content and page:
            if content == page.content: # Save needless versions being created.
                self.redirect('/wiki/{0}'.format(page_name))
            else:
                # Edit an existing page.
                page.content = content
                page.put()
                history = list(db.GqlQuery("SELECT * FROM WikiHistory WHERE page=:1 ORDER BY created DESC", page.key()))[0]
                new_history = WikiHistory(page=page, user=user, version=history.version+1, content=content)
                new_history.put()
                page = page_content(page_name, update=True)
                logging.info('User {0} edited wiki page {1} | {2}'.format(user.username, page_name, str(self.request)))
                self.redirect('/wiki/{0}'.format(page_name))
        elif content and not page:
            # Create a new page, plus history.
            page = Wiki(name=page_name, user=user, content=content)
            page.put()
            history = WikiHistory(page=page, user=user, version=1, content=content)
            history.put()
            logging.info('User {0} created wiki page {1} | {2}'.format(user.username, page_name, str(self.request)))
            self.redirect('/wiki/{0}'.format(page_name))
        else:
            error = 'Please input some content!'
            self.render('edit_wiki.html', name=page_name, error=error)


class PageHistory(asciichan.Handler):
    def get(self, page_name):
        user = get_user(self.request)
        page_name = page_name[1:]
        page = page_content(page_name)
        if page:
            history = db.GqlQuery("SELECT * FROM WikiHistory WHERE page=:1 ORDER BY created DESC", page.key())
            history = list(history)
            self.render('wiki_history.html', user=user, page=page, history=history)
        elif user and not page:
            self.redirect('/wiki/_edit/{0}'.format(page_name))
        else:
            self.render('wiki_blank.html', name=page_name)

        
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
    ('/wiki', WikiPage),
    ('/wiki/signup', auth.UserSignup),
    ('/wiki/login', auth.UserLogin),
    ('/wiki/logout', auth.UserLogout),
    ('/wiki/_edit' + PAGE_RE, EditPage),
    ('/wiki/_history' + PAGE_RE, PageHistory),
    ('/wiki/_edit', EditPage),
    ('/wiki' + PAGE_RE, WikiPage),
    ]

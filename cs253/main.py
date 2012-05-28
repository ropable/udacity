import sys
sys.path.append('C:\\Python27\\udacity\\cs253')
import webapp2
import asciichan
import blog


class MainPage(asciichan.Handler):
    def get(self):
        self.render('front.html')


app = webapp2.WSGIApplication([('/', MainPage)] + blog.URLS + asciichan.URLS, debug=True)

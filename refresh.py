import cm

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class DataRefreshHandler(webapp.RequestHandler):
    def get(self):
        cm.run

application = webapp.WSGIApplication([('/data/refresh', DataRefreshHandler)], debug=True)
if __name__ == '__main__':
    run_wsgi_app(application)
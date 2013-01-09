#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):

    def get(self):
        
        self.response.out.write('<!DOCTYPE html>\n')
        self.response.out.write(template.render('template_html/html_head_decl.html',
                                                {'site_title':"rFactorHotlapsServer"}))                      
        self.response.out.write( '<html><body>\n')
        
        self.response.out.write(template.render('template_html/main.html',{}))
        self.response.out.write(template.render('template_html/javascript_decl.html',{}))

        self.response.out.write('</body></html>')

if __name__ == "__main__":

    application = webapp2.WSGIApplication([
                                          ('/', MainPage)
                                          ], debug=True)    
    run_wsgi_app(application)

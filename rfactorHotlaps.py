#!/usr/bin/env python

import logging
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import engine

class OpeningPage(webapp2.RequestHandler):
    
    head_params = {'site_title':"rFactorHotlapsServer",
                   'specific_style': '<link href="/css/carousel.css" rel="stylesheet">'}
    
    carousel_call = "    <script> !function ($) { $(function(){ $('#myCarousel').carousel({ interval: 3000}) }) }(window.jQuery) </script>"
    
    def get(self):
        
        self.response.out.write('<!DOCTYPE html>\n')
        self.response.out.write(template.render('template_html/html_head_decl.html', self.head_params))
        self.response.out.write( '<html><body style="background-image:url(/images/tarmac-texture.jpg); background-position: center top; background-size: cover;">\n')
        self.response.out.write(template.render('template_html/openingPage.html',{}))
        self.response.out.write(template.render('template_html/javascript_decl.html',{}))
        self.response.out.write(self.carousel_call)
        self.response.out.write('\n</body></html>')
        print ("test")
        

if __name__ == "__main__":

    logging.getLogger().setLevel(logging.DEBUG)
    
    application = webapp2.WSGIApplication([
                                          ('/', OpeningPage), 
                                          (r'/r/(.*)', engine.MainPage)
                                          ], debug=True)    
    run_wsgi_app(application)

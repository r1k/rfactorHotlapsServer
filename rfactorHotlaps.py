#!/usr/bin/env python

import logging
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import engine

class OpeningPage(webapp2.RequestHandler):
    
    def get(self):
        
        head_params = []
        head_params = {'site_title':"rFactorHotlapsServer",
                       'specific_style': '<link href="/css/carousel.css" rel="stylesheet">'}

        carousel_call = []
        carousel_call = "    <script> !function ($) { $(function(){ $('#myCarousel').carousel({ interval: 3000}) }) }(window.jQuery) </script>"

        self.response.out.write('<!DOCTYPE html>\n')
        self.response.out.write(template.render('template_html/html_head_decl.html', head_params))
        self.response.out.write( '<html><body style="background-image:url(/images/tarmac-texture.jpg); background-position: center top; background-size: cover;">\n')
        self.response.out.write(template.render('template_html/openingPage.html',{}))
        self.response.out.write(template.render('template_html/javascript_decl.html',{}))
        self.response.out.write(carousel_call)
        self.response.out.write('\n</body></html>')


app = webapp2.WSGIApplication([
                                ('/', OpeningPage), 
                                (r'/r/(.*)', engine.MainPage)
                                (r'/xml/(.*)', backend.XMLInterface)
                              ], debug=True) 

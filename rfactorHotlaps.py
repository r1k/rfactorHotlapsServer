#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class OpeningPage(webapp2.RequestHandler):
    
    pageStyle='<link href="/css/carousel.css" rel="stylesheet">'
    
    def get(self):
        
        self.response.out.write('<!DOCTYPE html>\n')
        self.response.out.write(template.render('template_html/html_head_decl.html',
                                                {'site_title':"rFactorHotlapsServer",
                                                 'specific_style':self.pageStyle}))
        
        self.response.out.write( '<html><body>\n')
        self.response.out.write(template.render('template_html/openingPage.html',{}))
        self.response.out.write(template.render('template_html/javascript_decl.html',{}))
        self.response.out.write("<script>\n"
                                "!function ($) {\n"
                                "$(function(){\n"
                                "$('#myCarousel').carousel()\n"
                                "})\n"
                                "}(window.jQuery)\n"
                                "</script>\n"
                                )
        self.response.out.write('</body></html>')
        
class MainPage(webapp2.RequestHandler):
    
    pageStyle = """<style>
          body {
            padding-top: 60px;
          }
        </style>"""
        
    def get(self):
        
        self.response.out.write('<!DOCTYPE html>\n')
        self.response.out.write(template.render('template_html/html_head_decl.html',
                                                {'site_title':"rFactorHotlapsServer",
                                                 'specific_style':self.pageStyle}))
                           
        self.response.out.write( '<html><body>\n')
        self.response.out.write(template.render('template_html/main.html',{}))
        self.response.out.write(template.render('template_html/javascript_decl.html',{}))
        self.response.out.write('</body></html>')


if __name__ == "__main__":

    application = webapp2.WSGIApplication([
                                          ('/', OpeningPage), 
                                          ('/r/', MainPage)
                                          ], debug=True)    
    run_wsgi_app(application)

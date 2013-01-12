import logging
import os
import datetime
import webapp2
from google.appengine.ext.webapp import template

def server_handler():
    return "servers"

def links_handler():
    return "links"

def help_handler():
    return "help!"

def credits_handler():
    return "hello"

class MainPage(webapp2.RequestHandler):
    
    head_params = {'site_title':'rFactorHotlapsServer',
                   'specific_style': '<style> body { padding-top: 60px; } </style><link href="/css/footer.css" rel="stylesheet">'}
        
    def get(self, url_ext):
                
        logging.debug(url_ext)
        
        self.response.out.write('<!DOCTYPE html>\n')
        self.response.out.write(template.render('template_html/html_head_decl.html', self.head_params))
        self.response.out.write(template.render('template_html/nav_bar.html',{}))
        self.response.out.write( '<html><body>\n<div id="wrap">')  
        
        if (url_ext ==''):
            pass
        
        elif (url_ext == 'welcome'):
            self.response.out.write(template.render('template_html/main.html',{}))
            
        elif (url_ext == 'servers'):
            self.response.out.write( server_handler() )
            
        elif (url_ext == 'charts'):
            pass
        
        elif (url_ext == 'links'):
            self.response.out.write( links_handler() )
            
        elif (url_ext == 'help'):
            self.response.out.write( help_handler() )
            
        elif (url_ext == 'credits'):
            self.response.out.write( credits_handler() )
            
        else:
            self.redirect('/r/')
            
        self.response.out.write('</div>')
        self.response.out.write(template.render('template_html/footer.html',{}))
        self.response.out.write(template.render('template_html/javascript_decl.html',{}))   
        self.response.out.write('</body></html>')
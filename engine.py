import logging
import os
import datetime
import webapp2
from google.appengine.ext.webapp import template
import serverstatus
import support_functions as sup

def welcome_handler():
    page_txt = "Fluffy Dedicated Servers"
    content = template.render('template_html/branding_bar.html',{'page':page_txt})
    content = content + template.render('template_html/welcome.html',{})
    return content

def server_handler():
    page_txt = "Fluffy Dedicated Servers"
    content = template.render('template_html/branding_bar.html',{'page':page_txt})
    si = serverstatus.serverInfo()
    srvrs = si.server_list
    srvrs.append(serverstatus.server_details(('DS1','Silverstone', 'Bus', 'Qualifying','-','Noddy and Big ears','<a href="http://localhost:8080">Home</a>','')))
    srvrs.append(serverstatus.server_details(('DS2','Monza', 'Chariot', 'Deathmatch','-','Ben Hur','<a href="http://localhost:8080">Home</a>','')))
    srvrs.append(serverstatus.server_details(('DS3','Milky Way', 'XWing', 'Qualifying','-','Darth','<a href="http://localhost:8080">Home</a>','')))
    srvrs.append(serverstatus.server_details(('DS4','Indianapolis', 'NASCAR', 'Turning Left','-','Dick Trickle','<a href="http://localhost:8080">Home</a>','')))
    pairs = sup.pairs(srvrs)
    content = content + template.render('template_html/server_status.html',{'pairs':pairs})
    return content

def links_handler():
    page_txt = "Links"
    content = template.render('template_html/branding_bar.html',{'page':page_txt})
    content = content + template.render('template_html/links.html',{})
    return content

def help_handler():
    page_txt = "Help"
    content = template.render('template_html/branding_bar.html',{'page':page_txt})
    content = content + template.render('template_html/help.html',{})
    return content

def credits_handler():
    page_txt = "Credits"
    content = template.render('template_html/branding_bar.html',{'page':page_txt})
    content = content + template.render('template_html/credits.html',{})
    return content

class MainPage(webapp2.RequestHandler):
    
    head_params = {'site_title':'rFactorHotlapsServer',
                   'specific_style': '<style> body { padding-top: 60px;} </style><link href="/css/footer.css" rel="stylesheet">'}
        
    def get(self, url_ext):
                
        logging.debug(url_ext)

        nav_bar_params = {}
        active_string = 'class="active"'
        
        content=""

        if (url_ext =='' or url_ext == 'welcome'):
            content = welcome_handler()
            nav_bar_params = {'menu1':active_string}
            
        elif (url_ext == 'servers'):
            content = server_handler()
            self.head_params['meta_extra'] = """<meta http-equiv="cache-control" content="no-cache">
                                                <meta http-equiv="pragma" content="no-cache">
                                                <meta http-equiv="expires" content="-1000">
                                                <meta http-equiv="refresh" content="20">"""
            nav_bar_params = {'menu2':active_string}
            
        elif (url_ext == 'charts'):
            nav_bar_params = {'menu3':active_string}
        
        elif (url_ext == 'links'):
            content = links_handler()
            nav_bar_params = {'menu4':active_string}
            
        elif (url_ext == 'help'):
            content = help_handler()
            nav_bar_params = {'menu5':active_string}
            
        elif (url_ext == 'credits'):
            content = credits_handler()
            nav_bar_params = {'menu6':active_string}
            
        else:
            self.redirect('/r/')


        self.response.out.write('<!DOCTYPE html>\n')
        self.response.out.write(template.render('template_html/html_head_decl.html', self.head_params))
        self.response.out.write( '<html><body>\n<div id="wrap">')
        self.response.out.write(template.render('template_html/nav_bar.html', nav_bar_params ))

        self.response.out.write(content)
            
        self.response.out.write('</div>')
        self.response.out.write(template.render('template_html/footer.html',{}))
        self.response.out.write(template.render('template_html/javascript_decl.html',{}))   
        self.response.out.write('</body></html>')
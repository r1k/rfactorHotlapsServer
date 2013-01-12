import webapp2
from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):
    
    head_params = {'site_title':'rFactorHotlapsServer',
                   'specific_style': '<style> body { padding-top: 60px; } </style><link href="/css/footer.css" rel="stylesheet">'}
        
    def get(self):
        
        self.response.out.write('<!DOCTYPE html>\n')
        self.response.out.write(template.render('template_html/html_head_decl.html', self.head_params))
                           
        self.response.out.write( '<html><body>\n')
        self.response.out.write(template.render('template_html/main.html',{}))
        self.response.out.write(template.render('template_html/javascript_decl.html',{}))
        self.response.out.write('</body></html>')
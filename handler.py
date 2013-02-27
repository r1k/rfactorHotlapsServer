import logging
import webapp2
from google.appengine.ext.webapp import template

import config
import data_store


class hdlr(webapp2.RequestHandler):

    # handler base class
    head_params = {}
    nav_bar_params = {}

    def __init__(self, request=None, response=None):
        super(hdlr, self).__init__(request=request, response=response)
        self.nav_bar_params = {}
        self.head_params = {'site_title': 'rFactorHotlapsServer',
                            'specific_style': '<style> body { padding-top: 60px;} </style><link href="/css/footer.css" rel="stylesheet">'}

    def render(self, content):
        self.response.out.write('<!DOCTYPE html>\n')

        self.response.out.write(
                template.render('template_html/html_head_decl.html',
                                self.head_params))

        self.response.out.write('<html><body>\n<div id="wrap">')

        self.response.out.write(
                template.render('template_html/nav_bar.html',
                                self.nav_bar_params))

        self.response.out.write(content)

        self.response.out.write('</div>\n')

        self.response.out.write(
            template.render('template_html/footer.html', {}))

        self.response.out.write(
            template.render('template_html/javascript_decl.html', {}))

        self.response.out.write('</body></html>')

    def check_for_root(self):
        data_store.leagues().add_new(config.root_node())

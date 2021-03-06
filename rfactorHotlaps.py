#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp import template

import logging
import config


class OpeningPage(webapp2.RequestHandler):

    back_ground = '<html><body style="background-image:url(/static/images/tarmac-texture.jpg); background-position: center top; background-size: cover;">\n'

    def get(self, *args):

        head_params = []
        head_params = {'site_title': config.site_title(),
                       'specific_style': '<link href="/static/css/carousel.css" rel="stylesheet">'}

        carousel_call = []
        carousel_call = "    <script> !function ($) { $(function(){ $('#myCarousel').carousel({ interval: 3000}) }) }(window.jQuery) </script>"

        self.response.out.write('<!DOCTYPE html>\n')
        self.response.out.write(template.render('template_html/html_head_decl.html', head_params))
        self.response.out.write(self.back_ground)
        self.response.out.write(template.render('template_html/openingPage.html', {}))
        self.response.out.write(template.render('template_html/javascript_decl.html', {}))
        self.response.out.write(carousel_call)
        self.response.out.write('\n</body></html>')


logging.getLogger().setLevel(logging.DEBUG)
app = webapp2.WSGIApplication([(r'/(.*)', OpeningPage)], debug=True)

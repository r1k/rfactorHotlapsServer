import logging
from google.appengine.ext.webapp import template

import handler

# handler class for the admin functions


class handler(handler.hdlr):

    def __init__(self, request=None, response=None):
        super(handler, self).__init__(request=request, response=response)

    def get(self, url_ext):

        self.check_for_root()

        logging.debug("admin_handler")
        logging.debug(url_ext)
        page_txt = "Admin"

        if url_ext.startswith('/'):
            url_ext = url_ext[1:]

        content = template.render('template_html/branding_bar.html', {'page': page_txt})

        if url_ext.startswith('lap_insert'):
            logging.debug("lap_insert")
            content += self.lap_insert()

        else:
            content += template.render('template_html/admin.html', {})

        logging.debug("done")
        self.render(content)

    def lap_insert(self):
        return template.render('template_html/admin_lap_insert.html', {})

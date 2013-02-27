import logging
from google.appengine.ext.webapp import template

import handler
import data_store
import config

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

        content = template.render('template_html/branding_bar.html',
                                 {'page': page_txt})

        if url_ext.startswith('lap_insert'):
            logging.debug("lap_insert")
            content += self.lap_insert()

        else:
            content += template.render('template_html/admin.html', {})

        self.render(content)

    def lap_insert(self):
        return template.render('template_html/admin_lap_insert.html', {})

    def post(self, url_ext):

        logging.info("post")

        lap_details = []
        self.check_for_root()

        if url_ext.startswith('/'):
            url_ext = url_ext[1:]

        if url_ext.startswith("lap_insert"):
            logging.info("lap time submitted")

            db_if = data_store.interface(config.root_node())

            lap_details.append(self.request.get("driverName"))
            lap_details.append(self.request.get("carClass"))
            lap_details.append(self.request.get("carName"))
            lap_details.append(self.request.get("trackName"))
            lap_details.append(float(self.request.get("firstSector")))
            lap_details.append(float(self.request.get("secondSector")))
            lap_details.append(float(self.request.get("totalTime")))

            logging.info(str(lap_details))

            db_if.add_lap_time(lap_details)

        self.redirect('/admin/')

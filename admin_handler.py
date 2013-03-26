import logging
import webapp2
from google.appengine.ext.webapp import template
import xml.etree.ElementTree as ET

import handler
import data_store
import serverstatus as ss

import config
import support_functions as sup


class handler(handler.hdlr):
    """ Handler class for the admin functions
    """
    def __init__(self, request=None, response=None):
        super(handler, self).__init__(request=request, response=response)

    def lap_insert(self):
        return template.render('template_html/admin_lap_insert.html', {})

    def serversPage(argsList):

        content = template.render('template_html/admin_servers.html',
                                  {})
        return content

    def get(self, url_ext):

        self.check_for_root()

        logging.info("admin_handler")
        logging.info(url_ext)
        page_txt = "Admin"

        url_split = url_ext.split('/')
        url_extras = []
        for x in url_split[1:]:
            if x != '':
                url_extras.append(x)
        if len(url_extras) == 0:
            url_extras.append('menu')

        content = template.render('template_html/branding_bar.html',
                                  {'page': page_txt})

        if url_extras[0] == 'servers':
            content += self.serversPage(url_extras[1:])

        elif url_extras[0] == 'lap_insert':
            logging.info("lap_insert")
            content += self.lap_insert()

        elif url_extras[0] == 'insert_dummy_data':
            logging.info("Inserting Dummy Data")

            db_if = data_store.interface(config.root_node())

            dummy_data = sup.create_dictionary(config.input_labels(),
                                               config.dummy_test_data())
            for data in dummy_data:
                db_if.add_lap_time(data)

            self.redirect('/admin/')
            return

        elif url_extras[0] == 'importfromfile':
            logging.debug("insert from file")
            content += template.render('template_html/importfromfile.html', {})

        else:
            content += template.render('template_html/admin.html', {})

        self.render(content)

    def post(self, url_ext):

        logging.info("post")

        lap_details = []
        self.check_for_root()

        if url_ext.startswith('/'):
            url_ext = url_ext[1:]

        if url_ext.startswith("lap_insert"):
            logging.info("lap time submitted")

            db_if = data_store.interface(config.root_node())

            lap_details['driverName'] = self.request.get("driverName")
            lap_details['carClass'] = self.request.get("carClass")
            lap_details['carName'] = self.request.get("carName")
            lap_details['trackName'] = self.request.get("trackName")
            lap_details['firstSec'] = float(self.request.get("firstSector"))
            lap_details['secondSec'] = float(self.request.get("secondSector"))
            lap_details['totalTime'] = float(self.request.get("totalTime"))

            logging.info(str(lap_details))

            db_if.add_lap_time(lap_details)

        elif url_ext.startswith("importfromfile"):

            xmlfile = self.request.POST.get('xmlfile').file.read()
            results = ET.fromstring(xmlfile)

            db_if = data_store.interface(config.root_node())

            for result in results:
                db_if.add_lap_time(sup.translateXMLdictionary(result.attrib))

        self.redirect('/admin/')


logging.getLogger().setLevel(logging.DEBUG)
app = webapp2.WSGIApplication([(r'/admin(.*)', handler)], debug=True)

import logging
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
import xml.etree.ElementTree as ET

import handler
import data_store
import serverstatus as ss

import config
import support_functions as sup


class handler(handler.hdlr):
    """
        Handler class for the admin functions
    """
    def __init__(self, request=None, response=None):
        super(handler, self).__init__(request=request, response=response)

    def lap_insert(self):
        return template.render('template_html/admin_lap_insert.html', {})

    def serversPage(self, argsList):

        activeSet = False
        ssi = ss.interface()
        serverList = ssi.getAllServers()

        for s in serverList:
            if (len(argsList)) and (s.name == argsList[0]):
                s.Active = True
                activeSet = True
            s.linkstring = "/admin/servers/" + s.name

        # this is so that we can add new servers
        newServer = ss.serverSetup()
        newServer.name = "+new"
        newServer.linkstring = "/admin/servers/"
        if not activeSet:
            newServer.Active = True
        serverList.append(newServer)
        logging.info(str(serverList))

        content = template.render('template_html/admin_servers.html',
                                  {'serverList': serverList})
        return content

    def get(self, url_ext):

        self.check_for_root()

        logging.info("admin_handler")
        logging.info(url_ext)
        page_txt = "Admin"

        content = template.render('template_html/branding_bar.html',
                                      {'page': page_txt})

        url_split = sup.url_split(url_ext)

        if len(url_split) == 0:
            content += template.render('template_html/admin.html', {})

        else:

            if url_split[0] == 'servers':
                content += self.serversPage(url_split[1:])

            elif url_split[0] == 'lap_insert':
                logging.info("lap_insert")

                content += self.lap_insert()

            elif url_split[0] == 'insert_dummy_data':
                logging.info("Inserting Dummy Data")

                dummy_data = sup.create_dictionary(config.input_labels(),
                                                   config.dummy_test_data())

                db_if = data_store.interface(config.root_node())
                for data in dummy_data:
                    db_if.add_lap_time(data)

                self.redirect('/admin/')

            elif url_split[0] == 'importfromfile':
                logging.debug("insert from file")

                content += template.render('template_html/importfromfile.html',
                                           {})

            else:
                self.redirect('/admin/')
                content += template.render('template_html/admin.html', {})

        self.render(content)

    def post(self, url_ext):

        logging.info("post")
        logging.info(url_ext)
        self.check_for_root()

        url_split = sup.url_split(url_ext)

        if len(url_split) == 0:
            self.redirect('/admin/')

        if url_split[0] == "lap_insert":
            logging.info("lap time submitted")

            lap_details = []
            lap_details['driverName'] = self.request.get("driverName")
            lap_details['carClass'] = self.request.get("carClass")
            lap_details['carName'] = self.request.get("carName")
            lap_details['trackName'] = self.request.get("trackName")
            lap_details['firstSec'] = float(self.request.get("firstSector"))
            lap_details['secondSec'] = float(self.request.get("secondSector"))
            lap_details['totalTime'] = float(self.request.get("totalTime"))
            logging.info(str(lap_details))

            db_if = data_store.interface(config.root_node())
            db_if.add_lap_time(lap_details)

            self.redirect('/admin/')

        elif url_split[0] == "importfromfile":
            logging.info("importfromfile")

            xmlfile = self.request.POST.get('xmlfile').file.read()
            results = ET.fromstring(xmlfile)

            db_if = data_store.interface(config.root_node())

            for result in results:
                db_if.add_lap_time(sup.translateXMLdictionary(result.attrib))

            self.redirect('/admin/')

        elif (
              (url_split[0] == "update_server") or
              (
                  (url_split[0] == "servers") and
                  (url_split[1] == "update_server")
              )
             ):

            logging.info("update_server")

            oldServerName = self.request.get("originalName")

            if self.request.get("button") == "delete":
                ss.interface().deleteServerByName(oldServerName)

            elif self.request.get("button") == "add":
                s = ss.interface().getServerByName(oldServerName)
                logging.info(s)
                if s is None:
                    logging.info("create new")
                    s = ss.serverSetup(name=self.request.get("nsame"))

                    logging.info("s is:" + str(s))

                s.name = self.request.get("name")
                s.track_name = self.request.get("track_name")
                s.car_class_name = self.request.get("car_class_name")
                s.description = self.request.get("description")

                if s.image != '':
                    s.imageBlob = ndb.BlobInfo(self.image)

                logging.info(str(s))
                s.put()

                self.redirect('/admin/servers/' + s.name)

            else:
                self.redirect('/admin/servers/')

        else:
            logging.info("other url:" + str(url_split))
            self.redirect('/admin/')


logging.getLogger().setLevel(logging.DEBUG)
app = webapp2.WSGIApplication([(r'/admin(.*)', handler)], debug=True)

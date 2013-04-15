#!/usr/bin/env python
import webapp2
from google.appengine.ext.webapp import template
import logging

import serverstatus as ss
import handler
import support_functions as sup


class handler(handler.hdlr):

    def serversPage(self, argsList, ext_ServerStatus):

        activeSet = False
        ssi = ss.interface()
        serverList = ssi.getAllServers()

        for s in serverList:
            if (len(argsList)) and (s.name == argsList[0]):
                s.Active = True
                activeSet = True
            s.linkstring = "/servers/" + s.name

        if not activeSet:
            serverList[0].Active = True
        logging.info(str(serverList))

        content = template.render('template_html/server_status.html',
                                  {'serverList': serverList})
        return content

    def get(self, url_ext):
        logging.debug("serverHandler")

        url_split = sup.url_split(url_ext)

        content = template.render('template_html/branding_bar.html',
                                  {'page': "Fluffy's Dedicated Servers"})

        martinsServerStatus = []  # ss.serverInfo().run()

        content += self.serversPage(url_split, martinsServerStatus)

        self.nav_bar_params = {'servers': 'class="active"'}
        self.render(content)


logging.getLogger().setLevel(logging.INFO)
app = webapp2.WSGIApplication([(r'/servers(.*)', handler)], debug=True)

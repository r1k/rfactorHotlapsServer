#!/usr/bin/env python
import webapp2
from google.appengine.ext.webapp import template
import logging

import serverstatus as ss
import handler
import support_functions as sup


class handler(handler.hdlr):

    def get(self, url_ext):
        logging.debug("serverHandler")

        url_split = sup.url_split(url_ext)

        num_args = len(url_split)

        content = template.render('template_html/branding_bar.html',
                                  {'page': "Fluffy Dedicated Servers"})

        si = ss.serverInfo()
        martinsServerStatus = si.run()

        serverQuery = ss.serverSetup.query()

        paired_status_list = []
        for se in serverQuery:
            for mss in martinsServerStatus:
                if se.name == mss.name:
                    paired_status_list.append((se, mss))
                    break

        if len(paired_status_list) > 0:

            #work out index of server
            if num_args == 0:
                url_split.append(paired_status_list[0].name)
                activeServerPage = paired_status_list[0]
            else:
                count = 0
                for s in paired_status_list:
                    if s[0].name == url_split[0]:
                        serverIndex = count
                        break
                    count += 1
                activeServerPage = paired_status_list[serverIndex]

            serverNameList = [i[0].name for i in paired_status_list]

            content += template.render('template_html/server_status.html',
                                       {'serverNameList': serverNameList,
                                        'activeServer': activeServerPage})

        self.nav_bar_params = {'servers': 'class="active"'}
        self.render(content)


logging.getLogger().setLevel(logging.INFO)
app = webapp2.WSGIApplication([(r'/servers(.*)', handler)], debug=True)

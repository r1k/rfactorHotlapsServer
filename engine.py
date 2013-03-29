import logging
import webapp2
from google.appengine.ext.webapp import template

import handler
import serverstatus
import support_functions as sup


def welcome_handler(url_ext):
    logging.debug("welcome_handler")
    page_txt = "Fluffy Dedicated Servers"
    content = template.render('template_html/branding_bar.html',
                              {'page': page_txt})
    content += template.render('template_html/welcome.html', {})
    return content


def server_handler(url_ext):
    logging.debug("server_handler")
    page_txt = "Fluffy Dedicated Servers"
    content = template.render('template_html/branding_bar.html',
                              {'page': page_txt})
    si = serverstatus.serverInfo()
    srvrs = si.run()
    #srvrs.append(serverstatus.server_details(
            #('DS1', 'Silverstone', 'Bus', 'Qualifying', '-',
             #'Noddy and Big ears',
             #'<a href="http://localhost:8080">Home</a>', '')))
    #srvrs.append(serverstatus.server_details(
            #('DS2', 'Monza', 'Chariot', 'Deathmatch', '-',
             #'Ben Hur', '<a href="http://localhost:8080">Home</a>', '')))
    #srvrs.append(serverstatus.server_details(
            #('DS3', 'Milky Way', 'XWing', 'Qualifying', '-',
             #'Darth', '<a href="http://localhost:8080">Home</a>', '')))
    #srvrs.append(serverstatus.server_details(
            #('DS4', 'Indianapolis', 'NASCAR', 'Turning Left', '-',
             #'Dick Trickle', '<a href="http://localhost:8080">Home</a>', '')))
    pairs = sup.pairs(srvrs)
    content += template.render('template_html/server_status.html',
                               {'pairs': pairs})
    return content


def links_handler(url_ext):
    logging.debug("links_handler")
    page_txt = "Links"
    content = template.render('template_html/branding_bar.html',
                              {'page': page_txt})
    content += template.render('template_html/links.html', {})
    return content


def help_handler(url_ext):
    logging.debug("help_handler")
    page_txt = "Help"
    content = template.render('template_html/branding_bar.html',
                              {'page': page_txt})
    content += template.render('template_html/help.html', {})
    return content


def credits_handler(url_ext):
    logging.debug("credits_handler")
    page_txt = "Credits"
    content = template.render('template_html/branding_bar.html',
                              {'page': page_txt})
    content += template.render('template_html/credits.html', {})
    return content


class urlHandler(handler.hdlr):

    handlers = {'welcome': welcome_handler,
                'servers': server_handler,
                'links': links_handler,
                'help': help_handler,
                'credits': credits_handler}

    def __init__(self, request=None, response=None):
        super(urlHandler, self).__init__(request=request, response=response)

    def get(self, url_ext):
        logging.debug(url_ext)

        self.check_for_root()

        url_split = sup.url_split(url_ext)
        url_root = ''.join(url_split[0:1])  # this works if the list is empty

        content = ""

        if (url_root in self.handlers):
            content = self.handlers[url_root](url_split[1:])
        else:
            self.redirect('/r/welcome')

        if (url_root == 'servers'):
            self.head_params['meta_extra'] = \
                """<meta http-equiv="cache-control" content="no-cache">
                   <meta http-equiv="pragma" content="no-cache">
                   <meta http-equiv="expires" content="-1000">
                   <meta http-equiv="refresh" content="200">"""

        self.nav_bar_params = {url_root: 'class="active"'}
        self.render(content)


logging.getLogger().setLevel(logging.DEBUG)
app = webapp2.WSGIApplication([(r'/r/(.*)', urlHandler)], debug=True)

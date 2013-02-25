import logging
from google.appengine.ext.webapp import template

import handler
import serverstatus
import support_functions as sup
import data_store
import config


def welcome_handler(url_ext):
    logging.debug("welcome_handler")
    page_txt = "Fluffy Dedicated Servers"
    content = template.render('template_html/branding_bar.html', {'page': page_txt})
    content += template.render('template_html/welcome.html', {})
    return content

def server_handler(url_ext):
    logging.debug("server_handler")
    page_txt = "Fluffy Dedicated Servers"
    content = template.render('template_html/branding_bar.html', {'page': page_txt})
    si = serverstatus.serverInfo()
    srvrs = si.run()
    #srvrs.append(serverstatus.server_details(('DS1', 'Silverstone', 'Bus', 'Qualifying', '-', 'Noddy and Big ears', '<a href="http://localhost:8080">Home</a>', '')))
    #srvrs.append(serverstatus.server_details(('DS2', 'Monza', 'Chariot', 'Deathmatch', '-', 'Ben Hur', '<a href="http://localhost:8080">Home</a>', '')))
    #srvrs.append(serverstatus.server_details(('DS3', 'Milky Way', 'XWing', 'Qualifying', '-', 'Darth', '<a href="http://localhost:8080">Home</a>', '')))
    #srvrs.append(serverstatus.server_details(('DS4', 'Indianapolis', 'NASCAR', 'Turning Left', '-', 'Dick Trickle', '<a href="http://localhost:8080">Home</a>', '')))
    pairs = sup.pairs(srvrs)
    content += template.render('template_html/server_status.html', {'pairs': pairs})
    return content


def links_handler(url_ext):
    logging.debug("links_handler")
    page_txt = "Links"
    content = template.render('template_html/branding_bar.html', {'page': page_txt})
    content += template.render('template_html/links.html', {})
    return content


def help_handler(url_ext):
    logging.debug("help_handler")
    page_txt = "Help"
    content = template.render('template_html/branding_bar.html', {'page': page_txt})
    content += template.render('template_html/help.html', {})
    return content


def credits_handler(url_ext):
    logging.debug("credits_handler")
    page_txt = "Credits"
    content = template.render('template_html/branding_bar.html', {'page': page_txt})
    content += template.render('template_html/credits.html', {})
    return content


def charts_handler(url_ext):

    db_if = data_store.lap_datastore_interface(config.root_node())

    temp = ""

    if len(url_ext) == 0:
        #generate html containing top times for each track found
        tracks = data_store.lap_datastore_interface.get_tracks()
        for track in tracks:
            temp += template.render('template_html/track_result.html', {})

    elif url_ext[:5] == 'track':
        #generate list of times for a specific track
        pass

    elif url_ext[:9] == 'tanddhist':
        #list all times for a specific driver on a specific track
        track_list = db_if.get_tracks()

        for t in track_list:
            lap_times = db_if.get_best_times(t)
            tr = sup.track_results(lap_times)

    return temp


class urlHandler(handler.hdlr):

    handlers = {}

    def __init__(self, request=None, response=None):
        super(urlHandler, self).__init__(request=request, response=response)

        self.handlers['welcome'] = welcome_handler
        self.handlers['servers'] = server_handler
        self.handlers['charts'] = charts_handler
        self.handlers['links'] = links_handler
        self.handlers['help'] = help_handler
        self.handlers['credits'] = credits_handler

    def get(self, url_ext):

        self.check_for_root()

        logging.debug(url_ext)

        url_split = url_ext.split('/')
        url_root = url_split[0]
        url_extras = ''.join(url_split[1:])

        active_string = 'class="active"'
        content = ""

        if (url_root in self.handlers):
            content = self.handlers[url_root](''.join(url_extras))
        else:
            self.redirect('/r/welcome')

        if (url_root == 'servers'):
            self.head_params['meta_extra'] = """<meta http-equiv="cache-control" content="no-cache">
                                           <meta http-equiv="pragma" content="no-cache">
                                           <meta http-equiv="expires" content="-1000">
                                           <meta http-equiv="refresh" content="200">"""

        self.nav_bar_params = {url_root: active_string}
        self.render(content)


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


def charts_handler(url_ext):
    logging.info("charts_handler")

    content = ""
    logging.info(str(url_ext))

    trax = data_store.tracks(config.root_node())
    num_args = len(url_ext)
    if num_args == 0:
        #generate html containing top times for each track found
        logging.info('list all')
        for t in trax.get_all():
            trackname = t.get_name()
            logging.debug(trackname)
            cclass = data_store.carclass(t)
            for cc in cclass.get_all_names():
                logging.debug(cc)
                db_if = data_store.interface(trax.league_entity)
                laps = db_if.get_lap_times(trackname, cc)
                result_list = []
                for l in laps:
                    logging.debug(l)
                    result_list.append(sup.lap_result.from_lap_record(l))

                result_list = sup.calculate_lap_diffs(result_list)
                content += template.render('template_html/track_result.html',
                                           {'result_list': result_list,
                                            'trackname': trackname,
                                            'carclassname': cc})

    elif num_args == 1:
        #generate list of lap times for a specific track
        logging.info('list by track')
        trackname = url_ext[0]
        t = trax.get_by_name(trackname)
        cclass = data_store.carclass(t)
        for cc in cclass.get_all_names():
            logging.debug(cc)
            db_if = data_store.interface(trax.league_entity)
            laps = db_if.get_lap_times(trackname, cc)
            result_list = []
            for l in laps:
                logging.debug(l)
                result_list.append(sup.lap_result.from_lap_record(l))

            result_list = sup.calculate_lap_diffs(result_list)
            content += template.render('template_html/track_result.html',
                                       {'result_list': result_list,
                                        'trackname': trackname,
                                        'carclassname': cc})

    elif num_args == 2:
        #list all times for a specific track and car class
        logging.info('list by track and car class')
        trackname = url_ext[0]
        cc = url_ext[1]
        db_if = data_store.interface(trax.league_entity)
        laps = db_if.get_lap_times(trackname, cc)
        result_list = []
        for l in laps:
            logging.debug(l)
            result_list.append(sup.lap_result.from_lap_record(l))

        result_list = sup.calculate_lap_diffs(result_list)
        content += template.render('template_html/track_result.html',
                                   {'result_list': result_list,
                                    'trackname': trackname,
                                    'carclassname': cc})

    elif num_args == 3:
        #list all the times for a specific track, car class, and driver
        pass

    return content


class urlHandler(handler.hdlr):

    handlers = {}

    def __init__(self, request=None, response=None):
        super(urlHandler, self).__init__(request=request, response=response)

        self.handlers = {}
        self.handlers['welcome'] = welcome_handler
        self.handlers['servers'] = server_handler
        self.handlers['charts'] = charts_handler
        self.handlers['links'] = links_handler
        self.handlers['help'] = help_handler
        self.handlers['credits'] = credits_handler

    def get(self, url_ext):
        logging.debug(url_ext)

        self.check_for_root()

        url_split = url_ext.split('/')
        url_root = url_split[0]
        url_extras = []
        for x in url_split[1:]:
            if x != '':
                url_extras.append(x)

        content = ""

        if (url_root in self.handlers):
            content = self.handlers[url_root](url_extras)
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

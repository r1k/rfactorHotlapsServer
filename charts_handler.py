import logging
from google.appengine.ext.webapp import template

import handler
import data_store
import config
import support_functions as sup


def genResultList(l_name, t_name, c_name):
    laps = data_store.interface(l_name).get_lap_times(t_name, c_name)
    return sup.calculate_lap_diffs(
                [sup.lap_result.from_lap_record(l) for l in laps])


def genClassList(l_name, t_name, c_name, base_url):
    template_params = {'trackname': t_name,
                       'carclassname': c_name,
                       'track_url': base_url + t_name,
                       'track_clas_url': base_url + t_name + '/' + c_name}
    template_params['result_list'] = genResultList(l_name, t_name, c_name)
    return template.render('template_html/track_result.html', template_params)


def genTrackList(l_name, t_entity, base_url):
    t_name = t_entity.get_name()
    cclasses = data_store.carclass(t_entity)
    html = ""
    for c_name in cclasses.get_all_names():
        html += genClassList(l_name, t_name, c_name, base_url)
    return html


class handler(handler.hdlr):

    def __init__(self, request=None, response=None):
        super(handler, self).__init__(request=request, response=response)

    def get(self, url_ext):
        self.check_for_root()

        logging.debug("charts_handler")
        logging.debug(url_ext)
        content = template.render('template_html/branding_bar.html',
                                  {'page': "Charts"})

        url_split = url_ext.split('/')
        url_extras = []
        for x in url_split[1:]:
            if x != '':
                url_extras.append(x)

        l_name = config.root_node()
        tracks_if = data_store.tracks(l_name)

        num_args = len(url_extras)
        if num_args == 0:
            #generate html containing top times for each track found
            logging.info('list all')
            for t_entity in tracks_if.get_all():
                content += genTrackList(l_name,
                                        t_entity,
                                        base_url='./charts/')

        elif num_args == 1:
            #generate list of lap times for a specific track
            logging.info('list by track')
            content += genTrackList(l_name,
                                    tracks_if.get_by_name(url_extras[0]),
                                    base_url='')

        elif num_args == 2:
            #list all times for a specific track and car class
            logging.info('list by track and car class')
            content += genClassList(l_name,
                                    url_extras[0],
                                    url_extras[1],
                                    base_url='../')

        elif num_args == 3:
            #list all the times for a specific track, car class, and driver
            pass

        self.render(content)
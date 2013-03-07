import logging
import webapp2
from google.appengine.ext.webapp import template

import handler
import data_store
import config
import support_functions as sup


def genResultList(l_name,
                  t_name,
                  c_name,
                  d_name='everyone',):
    laps = data_store.interface(l_name)\
                .get_lap_times(t_name, c_name, driver_name=d_name)
    logging.debug(str(laps))
    return sup.calculate_lap_diffs(
                [sup.lap_result.from_lap_record(l) for l in laps])


def genFastestResultList(l_name,
                         t_name,
                         c_name,
                         d_name='everyone',):
    laps = data_store.interface(l_name)\
                .get_fastest_lap_times(t_name, c_name, driver_name=d_name)
    logging.debug(str(laps))
    return sup.calculate_lap_diffs(
                [sup.lap_result.from_lap_record(l.lap.get()) for l in laps])


def genClassList(l_name,
                 t_name,
                 c_name,
                 base_url,
                 d_name='everyone',
                 list_gen=genFastestResultList,
                 template_html='template_html/track_result.html'):

    track_url = base_url + t_name
    class_url = track_url + '/' + c_name
    driver_url = class_url + '/'
    template_params = {'trackname': t_name,
                       'carclassname': c_name,
                       'track_url': track_url,
                       'track_clas_url': class_url,
                       'driver_url_base': driver_url}
    template_params['result_list'] = list_gen(l_name, t_name, c_name, d_name)
    logging.debug(str(template_params['result_list']))
    return template.render(template_html, template_params)


def genTrackList(l_name,
                 t_entity,
                 base_url,
                 d_name='everyone',
                 list_gen=genFastestResultList,
                 template_html='template_html/track_result.html'):
    t_name = t_entity.get_name()
    cclasses = data_store.carclass(t_entity)
    html = ""
    logging.debug(str(cclasses.get_all_names()))
    for c_name in cclasses.get_all_names():
        html += genClassList(l_name,
                             t_name,
                             c_name,
                             base_url,
                             d_name,
                             list_gen,
                             template_html)
    return html


class handler(handler.hdlr):

    def __init__(self, request=None, response=None):
        super(handler, self).__init__(request=request, response=response)

    def get(self, url_ext):
        self.check_for_root()

        logging.debug("charts_handler")
        logging.debug("Params: %s", url_ext)
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
        logging.debug("Num args: " + str(num_args) +
                      ', list: ' + str(url_extras))
        if num_args == 0:
            #generate html containing top times for each track found
            logging.debug('list all')
            t_list = tracks_if.get_all()
            logging.debug('track list: ' + str(t_list))
            for t_entity in tracks_if.get_all():
                logging.debug('track: ' + t_entity.get_name())
                content += genTrackList(l_name,
                                        t_entity,
                                        base_url='./',
                                        list_gen=genFastestResultList)

        elif num_args == 1:
            #generate list of lap times for a specific track
            logging.debug('list by track')
            content += genTrackList(l_name,
                                    tracks_if.get_by_name(url_extras[0]),
                                    base_url='./',
                                    list_gen=genFastestResultList)

        elif num_args == 2:
            #list all times for a specific track and car class
            logging.debug('list by track and car class')
            content += genClassList(l_name,
                                    url_extras[0],
                                    url_extras[1],
                                    base_url='../',
                                    list_gen=genResultList)

        elif num_args == 3:
            #list all the times for a specific track, car class, and driver
            logging.debug('list by track and car class and driver')
            content += genClassList(l_name,
                              url_extras[0],
                              url_extras[1],
                              base_url='../../',
                              d_name=url_extras[2],
                              list_gen=genResultList,
                              template_html='template_html/driver_result.html')

        self.render(content)


logging.getLogger().setLevel(logging.INFO)
app = webapp2.WSGIApplication([(r'/charts(.*)', handler)], debug=True)

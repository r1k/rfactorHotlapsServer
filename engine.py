import logging
import webapp2
from google.appengine.ext.webapp import template
import serverstatus
import support_functions as sup
import data_store


def welcome_handler():
    page_txt = "Fluffy Dedicated Servers"
    content = template.render('template_html/branding_bar.html', {'page': page_txt})
    content = content + template.render('template_html/welcome.html', {})
    return content


def server_handler():
    page_txt = "Fluffy Dedicated Servers"
    content = template.render('template_html/branding_bar.html', {'page': page_txt})
    si = serverstatus.serverInfo()
    srvrs = si.server_list
    srvrs.append(serverstatus.server_details(('DS1', 'Silverstone', 'Bus', 'Qualifying', '-', 'Noddy and Big ears', '<a href="http://localhost:8080">Home</a>', '')))
    srvrs.append(serverstatus.server_details(('DS2', 'Monza', 'Chariot', 'Deathmatch', '-', 'Ben Hur', '<a href="http://localhost:8080">Home</a>', '')))
    srvrs.append(serverstatus.server_details(('DS3', 'Milky Way', 'XWing', 'Qualifying', '-', 'Darth', '<a href="http://localhost:8080">Home</a>', '')))
    srvrs.append(serverstatus.server_details(('DS4', 'Indianapolis', 'NASCAR', 'Turning Left', '-', 'Dick Trickle', '<a href="http://localhost:8080">Home</a>', '')))
    pairs = sup.pairs(srvrs)
    content = content + template.render('template_html/server_status.html', {'pairs': pairs})
    return content


def links_handler():
    page_txt = "Links"
    content = template.render('template_html/branding_bar.html', {'page': page_txt})
    content = content + template.render('template_html/links.html', {})
    return content


def help_handler():
    page_txt = "Help"
    content = template.render('template_html/branding_bar.html', {'page': page_txt})
    content = content + template.render('template_html/help.html', {})
    return content


def credits_handler():
    page_txt = "Credits"
    content = template.render('template_html/branding_bar.html', {'page': page_txt})
    content = content + template.render('template_html/credits.html', {})
    return content


def admin_handler(url):
    page_txt = "Admin"
    content = template.render('template_html/branding_bar.html', {'page': page_txt})
    if (url == 'lap_insert'):
        content = content + template.render('template_html/admin_lap_insert.html', {})
    return content


class charts_handler():

    db_if = None

    def __init__(self, league):
        self.db_if = data_store.lap_datastore_interface(league)

    def process(self, params):
        if len(params) == 0:
            #generate html containing top times for each track found
            pass
        elif params[:5] == 'track':
            #generate list of times for a specific track
            pass
        elif params[:9] == 'tanddhist':
            #list all times for a specific driver on a specific track
            track_list = self.db_if.get_tracks()

            for t in track_list:
                lap_times = self.db_if.get_best_times(t)
                tr = sup.track_results(lap_times)


class MainPage(webapp2.RequestHandler):

    root_node_name = 'league'

    def get(self, url_ext):

        if not data_store.league.get_by_key_name(self.root_node_name):
            # Populate db on first run
            root = data_store.league(key_name=self.root_node_name)
            root.put()

        head_params = []
        head_params = {'site_title': 'rFactorHotlapsServer',
                   'specific_style': '<style> body { padding-top: 60px;} </style><link href="/css/footer.css" rel="stylesheet">'}

        logging.debug(url_ext)

        nav_bar_params = {}
        active_string = 'class="active"'

        content = ""

        if (url_ext == '' or url_ext == 'welcome'):
            content = welcome_handler()
            nav_bar_params = {'menu1': active_string}

        elif (url_ext == 'servers'):
            content = server_handler()
            head_params['meta_extra'] = """<meta http-equiv="cache-control" content="no-cache">
                                                <meta http-equiv="pragma" content="no-cache">
                                                <meta http-equiv="expires" content="-1000">
                                                <meta http-equiv="refresh" content="20">"""
            nav_bar_params = {'menu2': active_string}

        elif (url_ext == 'charts'):
            handler = charts_handler(self.root_node_name)
            content = handler.process(url_ext[6:])
            nav_bar_params = {'menu3': active_string}

        elif (url_ext == 'links'):
            content = links_handler()
            nav_bar_params = {'menu4': active_string}

        elif (url_ext == 'help'):
            content = help_handler()
            nav_bar_params = {'menu5': active_string}

        elif (url_ext == 'credits'):
            content = credits_handler()
            nav_bar_params = {'menu6': active_string}

        elif (url_ext[:5] == 'admin'):
            content = admin_handler(url_ext[6:])

        else:
            self.redirect('/r/')

        self.response.out.write('<!DOCTYPE html>\n')
        self.response.out.write(template.render('template_html/html_head_decl.html', head_params))
        self.response.out.write('<html><body>\n<div id="wrap">')
        self.response.out.write(template.render('template_html/nav_bar.html', nav_bar_params))
        self.response.out.write(content)
        self.response.out.write('</div>')
        self.response.out.write(template.render('template_html/footer.html', {}))
        self.response.out.write(template.render('template_html/javascript_decl.html', {}))
        self.response.out.write('</body></html>')

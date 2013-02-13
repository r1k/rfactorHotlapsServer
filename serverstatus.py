import urllib2
from HTMLParser import HTMLParser
import logging


class server_details():

    details = []
    name = ''
    image = ''
    track = ''
    vclass = ''
    seshtype = ''
    seshstatus = ''
    driverlist = ''
    extras = 7

    def __init__(self, dtls):
        self.details = dtls
        self.name = dtls[0]
        self.image = dtls[1]
        self.track = dtls[2]
        self.vclass = dtls[3]
        self.seshtype = dtls[4]
        self.seshstatus = dtls[5]
        self.driverlist = dtls[6]

    def __str__(self):

        string = []
        for i in self.details:
            if len(string) != 0:
                string = string + ', ' + i
            else:
                string = i

        return string


class serverParser(HTMLParser):

    servers = []
    content = []

    collecting_data = 0
    field = 0

    server_url = ''

    def clear_vars(self):
        self.server_url = ''
        self.servers = []
        self.content = []
        self.field = 0
        self.collecting_data = False

    def handle_starttag(self, tag, attrs):
        if tag == 'ul':
            self.collecting_data = 1
            self.field = 0

        if tag == 'li' and self.collecting_data == 1:
            self.collecting_data = 2

    def handle_endtag(self, tag):
        if self.collecting_data > 0:
            if tag == 'ul':
                self.collecting_data = 0
                self.servers.append(server_details(self.content))
                self.content = []
            elif tag == 'li':
                self.collecting_data = 1

    def handle_data(self, data):
        if self.collecting_data == 2:
            self.content.append(data.strip())


class serverInfo():

    url = 'http://nodb.homeserver.com/rfactor/servers.asp'
    test_file = []
    server_list = []
    server_status_html = []

    def __init__(self):

        self.server_list = []
        self.server_status_html = []
        self.test_file = []

    def run(self):

        self.open_url(self.url)
        self.parse_html()

    def test(self, test_filename):

        self.open_test_file(test_filename)
        self.parse_html()

    def open_url(self, url):
        try:
            uo = urllib2.urlopen(self.url)

            self.server_status_html = uo.read()

        except Exception:
            logging.warning("Unable to read server status")
            return

    def open_test_file(self, tf):
        f = open(tf, 'r')
        self.server_status_html = f.read()

    def parse_html(self):
        sp = serverParser()
        sp.clear_vars()
        sp.feed(self.server_status_html)

        self.server_list = sp.servers

        for s in self.server_list:
            logging.debug(s)


if __name__ == "__main__":

    #debug mode

    test_files = ('test_src/serverstatus/pc_booted-loading-cannot_join.htm',
                  'test_src/serverstatus/pc_booted-running-user_can_join.htm',
                  'test_src/serverstatus/pc_booting-cannot-join.htm',
                  'test_src/serverstatus/pc_offline-cannot_join.htm')

    for test in test_files:
        si = serverInfo()
        si.test(test)

        for sr in si.server_list:
            print(sr)

import urllib2
from google.appengine.ext import ndb
from HTMLParser import HTMLParser
import logging


class serverSetup(ndb.Model):
    # data store object to store static data store details
    name = ndb.StringProperty(required=True)
    track_name = ndb.StringProperty()
    car_class_name = ndb.StringProperty()
    description = ndb.TextProperty()
    #image = ndb.BlobProperty()


class interface:
    def __init__(self):
        pass

    def getAllServers_iter(self):
        q = serverSetup.query().order(serverSetup.name)
        return q.iter

    def getAllServers(self, num_results=5):
        q = serverSetup.query().order(serverSetup.name)
        return q.fetch(num_results)

    def getAllServerNames(self, num_results=5):
        q = serverSetup.query().order(serverSetup.name)
        return q.fetch(num_results, projection=[serverSetup.name])

    def getServerByName(self, name):
        q = serverSetup.query().filter(serverSetup.name == name)
        return q.fetch(1)

    def addServer(self, serverDetails):
        ss = serverSetup(name=serverDetails.name)
        # fill in other server details
        ss.put()

    def updateServer(self, server, serverDetails):
        if server is not serverSetup:
            logging.error('Need a serverSetup object to be able to update it')
            return
        # copy over all serverDetails and then push back to db
        server.put()


class server_details():

    def __init__(self, dtls):
        self.details = dtls[self.extras:]
        self.name = dtls[0]
        self.image = dtls[1]
        self.track = dtls[2]
        self.vclass = dtls[3]
        self.seshtype = dtls[4]
        self.seshstatus = dtls[5]
        self.driverlist = dtls[6]
        self.total_rows = len(dtls) - 1
        self.extras = 7

    def __str__(self):
        string = self.name + ', ' +\
                 self.image + ', ' +\
                 self.track + ', ' +\
                 self.vclass + ', ' +\
                 self.seshtype + ', ' +\
                 self.seshstatus + ', ' +\
                 self.driverlist

        for i in self.details:
                string = string + ', ' + i

        return string

    def rebuild_links(self):
        #only need to check extra links
        string = ""
        local_details = []

        for d in self.details:
            if 'rfactor://' in d:
                string = '<a href="' + d + '">Join Server</a>'
            elif 'live.asp' in d:
                string = '<a href="' + d + '">Live stats</a>'
            elif 'rfactor/woli' in d:
                string = '<a href="' + d + '">Start Server PC</a>'
            else:
                string = d
            local_details.append(string)

        self.details = local_details


class serverParser(HTMLParser):

    def __init__(self):
        self.servers = []
        self.content = []
        self.collecting_data = 0
        self.field = 0
        self.server_url = ''

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

    url = 'http://nodb.homeserver.com/rfactor/serversNew.asp'

    def __init__(self):
        self.server_list = []
        self.server_status_html = ""
        self.test_file = ""

    def run(self):
        self.open_url(self.url)
        self.parse_html()
        return self.server_list

    def test(self, test_filename):
        self.open_test_file(test_filename)
        self.parse_html()
        return self.server_list

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
            s.rebuild_links()
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

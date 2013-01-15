import urllib2
from HTMLParser import HTMLParser
import logging

class server_details():
    
    name = ''
    track = ''
    vclass = ''
    seshtype = ''
    seshstatus = ''
    driverlist = ''
    server = ''
    options = ''
    
    def __init__( self, details ):
        self.name = details[0]
        self.track = details[1]
        self.vclass = details[2]
        self.seshtype = details[3]
        self.seshstatus = details[4]
        self.driverlist = details[5]
        self.server = details[6]
        self.options = details[7]
        
    def __str__(self):
        
        return self.name + ', ' + self.track + ', ' + self.vclass + ', ' + self.seshtype + ', ' + self.seshstatus + ', ' + self.driverlist + ', ' + self.server

class serverParser(HTMLParser):
    
    servers = []
    content = []
        
    collecting_data = False
    field = 0
    
    server_url = ''
    
    def clear_vars(self):
        self.server_url = ''
        self.servers = []
        self.content = []
        self.field = 0
        self.collecting_data = False
    
    def handle_starttag(self, tag, attrs):
        if self.collecting_data:
            if tag == 'a':
                url='#'
                for attr in attrs:
                    if attr[0] == 'href':
                        url = attr[1]
                        break
                self.server_url = url
                    
        if tag == 'table':
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'result':
                    self.collecting_data = True
                    self.field = 0
                    break
        
            
    def handle_endtag(self, tag):
        if tag == 'table' and self.collecting_data == True:
            self.collecting_data = False
            self.servers.append(server_details(self.content))
            self.content = []
            
    
    def handle_data(self, data):
        if self.collecting_data:
            if (self.field < 12) and ((self.field % 2) == 0) :
                self.content.append(data)
            elif self.field == 12:
                self.content.append(self.server_url)
                self.content.append(data)
            self.field = self.field + 1
    
    
    
class serverInfo():
    
    url = 'http://nodb.homeserver.com/rfactor/servers.asp'
    url2= 'http://nodb.homeserver.com/rfactor/'
    martins_html = []
    server_list = []
    
    def __init__(self):
       
        self.server_list = []
        try:
            uo = urllib2.urlopen(self.url)
            
            self.martins_html = uo.read()
            
        except Exception:
            print "Unable to read server status"
            return
                
        sp = serverParser()
        sp.clear_vars()
        sp.feed(self.martins_html)
        
        self.server_list = sp.servers
        
        #logging.debug( 'Number :' + str(len(self.server_list)))
        #for s in self.server_list:
        #    logging.debug( s )
        
        for s in self.server_list:
            s.server = "<a href='" + self.url2 + s.server + "'>" + s.options + "</a>"

        
if __name__ == "__main__":
    
    #debug mode

    si = serverInfo()
    
    for sr in si.server_list:
        print sr

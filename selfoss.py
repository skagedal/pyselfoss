import httplib
import urllib
import json

class Item:
    def __init__(self, selfoss, data):
        self.selfoss = selfoss
        self.data = data
        self.id = data['id']
        self.unread = data['unread'] == u'1'
        self.starred = data['starred'] == u'1'

    def mark(self):
        ret = self.selfoss.mark(self.id)
        if ret['success']:
            self.unread = False

    def unmark(self):
        ret = self.selfoss.unmark(self.id)
        if ret['success']:
            self.unread = True

class Selfoss:
    def __init__(self, server, base):
        self.server = server
        self.base = base

    def request(self, method, command, params = {}):
        data = None
        params = urllib.urlencode(params)
        conn = httplib.HTTPConnection(self.server)
        conn.request(method, self.base + command, params)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read()

        conn.close()
        if data is not None:
            return json.loads(data)
        else:
            raise Error("couldn't process request")

    def GET(self, command, params = {}):
        return self.request("GET", command, params)

    def POST(self, command, params = {}):
        return self.request("POST", command, params)

    def sources(self):
        return self.GET("/sources/list")

    def items(self, **kwargs):
        """List items. Optional keyword arguments:
           """
        return [Item(self, data) for data in self.GET("/items")]

    def mark(self, item_id):
        return self.POST("/mark/%s" % item_id)

    def unmark(self, item_id):
        return self.POST("/unmark/%s" % item_id)

    

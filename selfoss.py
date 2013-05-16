from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import urllib
import json
import datetime
if sys.version_info[0] >= 3:
    import http.client
    httplib = http.client
    urlencode = urllib.parse.urlencode
else:
    import httplib
    urlencode = urllib.urlencode


class Item:
    def __init__(self, selfoss, data):
        self.selfoss = selfoss
        self.data = data

        self.id = data['id']
        self.datetime = datetime.datetime.strptime(data['datetime'], "%Y-%m-%d %H:%M:%S")
        self.title = data['title']
        self.content = data['content']
        self.unread = data['unread'] == u'1'
        self.starred = data['starred'] == u'1'
        self.source = data['source']
        self.thumbnail = data['thumbnail']
        self.icon = data['icon']
        self.uid = data['uid']
        self.link = data['link']
        self.sourcetitle = data['sourcetitle']
        self.tags = data['tags']

    def __repr__(self):
        return "<Item %s: %s>" % (self.id, self.title)

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
        params = urlencode(params)
        conn = httplib.HTTPConnection(self.server)
        conn.request(method, self.base + command, params)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read().decode('utf-8')

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
        params = {}
        for key in ["type", "search", "tag", "source", "offset", "items"]:
            if key in kwargs:
                params[key] = kwargs[key]
        return [Item(self, data) for data in self.GET("/items", params)]

    def mark(self, item_id):
        return self.POST("/mark/%s" % item_id)

    def unmark(self, item_id):
        return self.POST("/unmark/%s" % item_id)

    
local = Selfoss('localhost', '/simon/selfoss')

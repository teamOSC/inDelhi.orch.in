#!/usr/bin/env python

import webapp2
import json
import urllib2
import urllib
import json
import logging
import hashlib
import jinja2
import os
import urlparse

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

def get_dict(**kwargs):
    d= {}
    for k,v in kwargs.iteritems():
        d[k] = v
    return d

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/doc.html')
        self.response.out.write(template.render())

class View(webapp2.RequestHandler):
    def get(self):
        url = "https://spreadsheets.google.com/feeds/list/1fze77rkhUkF2jCcSzdy9-ytcspUmb8r3aGLX84XBFGw/od6/public/values?alt=json"
        json_ob = json.loads(urllib2.urlopen(url).read())
        arr = []
        for i in json_ob["feed"]["entry"]:
            d= {}
            title = i["gsx$title"]["$t"]
            description = i["gsx$description"]["$t"]
            image = i["gsx$image"]["$t"]
            time = i["gsx$time"]["$t"]
            venue = i["gsx$venue"]["$t"]
            tags = i["gsx$tags"]["$t"]
            id = hashlib.md5(title,description,image).hexdigest()[:6]
            d = get_dict(id=id,title=title,description=description,image=image,time=time,venue=venue,tags=tags)
            arr.append(d)

        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render(arr=arr))


app = webapp2.WSGIApplication([
    ('/admin', MainHandler),
    ('/',View)
], debug=True)




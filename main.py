#!/usr/bin/env python

import webapp2
import json
import urllib2
import urllib
import json
import logging

import jinja2
import os
import urlparse

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])
    

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
            title = i["gsx$title"]["$t"]
            description = i["gsx$description"]["$t"]
            image = i["gsx$image"]["$t"]
            time = i["gsx$time"]["$t"]
            venue = i["gsx$venue"]["$t"]
            coordinates = i["gsx$coordinates"]["$t"]
            arr.append([title,description,image,time,venue,coordinates])

        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render(arr=arr))


app = webapp2.WSGIApplication([
    ('/admin', MainHandler),
    ('/',View)
], debug=True)




#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import codecs
import webapp2
import jinja2
from google.appengine.ext import db
#from check import valid_month
#from check import valid_year
#from check import valid_day

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape= True)

class Handler(webapp2.RequestHandler):
	"""docstring for Handler"""
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class Declare(db.Model):
	title = db.StringProperty( required=True)
	area = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)


class Secondhandler(Handler):
	def render_it(self, error="", title="", area=""):
		arts = db.GqlQuery("SELECT * FROM Declare "
							"ORDER BY created DESC ")
		self.render("shopping_list.html", error= error, title= title, area= area, arts = arts)
	
	def get(self):
		self.render_it()

	def post(self):
		title = self.request.get('title')
		area = self.request.get('ascii')

		if title and area:
			a = Declare( title= title, area = area)
			a.put()
			self.redirect("/")
		else:
			self.render_it(error = "error, plz put in title nd body both",title= title, area= area)



app = webapp2.WSGIApplication([
    ('/',Secondhandler)
], debug=True)

#!/usr/bin/env python
# MIT License
# (c) baltasar 2015

import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        msg = None

        try:
    	    msg = self.request.GET['msg']
        except:
            msg = None

    	if msg == None:
            msg = "CRITICAL - contact development team"

        template_values = {
			"error_msg": msg,
		}

        template = JINJA_ENVIRONMENT.get_template( "error.html" )
        self.response.write(template.render(template_values));

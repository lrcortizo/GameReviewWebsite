from google.appengine.api import users
from google.appengine.ext import ndb

import time
import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class RemoveCommentHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=Comment was not found")
            return
        user = users.get_current_user()

        if user != None:
            try:
                comment = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=Comment key was not found")
                return
            comment.key.delete()
            time.sleep(1)
            self.redirect("/")
        else:
            self.redirect("/")



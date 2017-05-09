from google.appengine.api import users
from google.appengine.ext import ndb

from game import Game

import time
import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class RemoveHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=Game was not found")
            return
        user = users.get_current_user()

        if user != None:
            try:
                game = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=Game key was not found")
                return
            game.key.delete()
            time.sleep(1)
            self.redirect("/usergames")
        else:
            self.redirect("/")



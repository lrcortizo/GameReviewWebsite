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

class UpdateHandler(webapp2.RequestHandler):
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
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                game = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=Game key does not exist")
                return

            template_values = {
    			"user_name": user_name,
    			"access_link": access_link,
    			"game": game,
    		}

            template = JINJA_ENVIRONMENT.get_template( "/views/update.html" )
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=Missing id for modification")
            return

        user = users.get_current_user()

        if user != None:
            try:
                game = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=Game key does not exist")
                return

            game.name = self.request.get("name").strip()
            game.description = self.request.get("description").strip()
            game.picture = self.request.get("picture").strip()
            game.web = self.request.get("web").strip()
            game.company = self.request.get("company").strip()

            game.put()
            time.sleep(1)
            self.redirect("/usergames")
        else:
            self.redirect("/")

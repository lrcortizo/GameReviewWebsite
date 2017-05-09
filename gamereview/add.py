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

class AddHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")
            template_values = {
                "user_name": user_name,
                "access_link": access_link,
            }

            template = JINJA_ENVIRONMENT.get_template("/views/add.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")

    def post(self):
        user = users.get_current_user()

        if user != None:
            game = Game()
            game.name = self.request.get("name").strip()
            game.user = user.user_id()
            game.description = self.request.get("description").strip()
            game.picture = self.request.get("picture").strip()
            game.web = self.request.get("web").strip()
            game.company = self.request.get("company").strip()
            games = Game.query()
            label = False
            for g in games:
                if g.name == game.name:
                    label = True
            if label == True:
                self.redirect("/error?msg=Game already exists")
                return
            else:
                game.put()
                time.sleep(1)
            self.redirect("/usergames")
        else:
            self.redirect("/")

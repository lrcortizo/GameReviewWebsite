from google.appengine.api import users

from game import Game

import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class UserGamesHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user == None:
            user_name = "Please login"
            access_link = users.create_login_url("/")
            template_values = {
                "user_name": user_name,
                "access_link": access_link,
            }


        else:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            #Se obtienen los juegos correspondientes al usuario actual
            games = Game.query(Game.user == user.user_id()).order(-Game.date)

            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "games": games,

            }

        template = JINJA_ENVIRONMENT.get_template("/views/usergames.html")
        self.response.write(template.render(template_values));
from game import Game
from comment import Comment
from google.appengine.api import users

import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class UserCommentsHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            #Se obtienen los juegos donde ha comentado el usuario actual
            comments = Comment.query(Comment.user == user.user_id())
            games = []
            for comment in comments:
                game = Game.query(comment.game == Game.key).get()
                if (game in games) == False:
                    games.append(game)

            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "games": games,
            }

            template = JINJA_ENVIRONMENT.get_template("/views/usergames.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")
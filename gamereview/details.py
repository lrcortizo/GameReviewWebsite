from google.appengine.api import users
from google.appengine.ext import ndb

from comment import Comment

import time
import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class DetailsHandler(webapp2.RequestHandler):
    def get(self):

        #Se comprueba que se corresponde con el id de un juego
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=Missing id for modification")
            return

        user = users.get_current_user()

        if user != None:
            # Se obtiene el juego
            try:
                game = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=Game key doesn't exist")
                return
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            #Se extraen los comentarios correspondientes
            comments = Comment.query(Comment.game == game.key).order(-Comment.date)
                
            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "game": game,
                "comments": comments,
                "iduser": user.user_id(),
            }

            template = JINJA_ENVIRONMENT.get_template("/views/details.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")
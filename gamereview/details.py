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

        # Se comprueba que se corresponde con el id de un juego
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=Missing id for modification")
            return

        user = users.get_current_user()

        # Comprobacion usuario
        if user != None:
            iduser = user.user_id()
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

        else:
            iduser = None
            user_name = "Please login"
            access_link = users.create_login_url("/")

        # Se obtiene el juego
        try:
            game = ndb.Key(urlsafe=id).get()
        except:
            self.redirect("/error?msg=Game key doesn't exist")
            return


        #Se extraen los comentarios correspondientes
        comments = Comment.query(Comment.game == game.key).order(-Comment.date)

        #Calcular la media
        v = 0
        cont = 0
        for c in comments:
            v += c.punctuation
            cont += 1
        if cont == 0:
            mean = 0
        else:
            mean = v/cont

        template_values = {
            "user_name": user_name,
            "access_link": access_link,
            "game": game,
            "comments": comments,
            "iduser": iduser,
            "mean": mean,
        }

        template = JINJA_ENVIRONMENT.get_template("/views/details.html")
        self.response.write(template.render(template_values));
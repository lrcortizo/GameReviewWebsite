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

class UpdateCommentHandler(webapp2.RequestHandler):
    def get(self):

        # Se comprueba que hay un id para el comentario
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=Comment was not found")
            return

        user = users.get_current_user()

        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")
            # Se obtiene el id del comentario
            try:
                comment = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=Comment key doesn't exist")
                return

            template_values = {
    			"user_name": user_name,
    			"access_link": access_link,
    			"comment": comment,
    		}

            template = JINJA_ENVIRONMENT.get_template( "/views/updatecomment.html" )
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")

    def post(self):
        #Se comprueba que hay un id para el comentario
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=Missing id for modification")
            return

        user = users.get_current_user()

        if user != None:
            # Se obtiene el id del comentario
            try:
                comment = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=Comment key does not exist")
                return

            if user.user_id() == comment.user:
                # Se obtienen los campos del formulario y se pasan al formato correcto
                comment.comment = self.request.get("comment").strip()
                comment.numHours = int(self.request.get("hours").strip())
                if "yes" == self.request.get("finished").strip():
                    comment.finished = True
                else:
                    comment.finished = False
                comment.punctuation = int(self.request.get("star"))

                #Se actualiza
                comment.put()
                time.sleep(1)
            else:
                self.redirect("/error?msg=You don't have premissions to do this")
                return

            #Redireccion
            game = Game.query(comment.game == Game.key).get()
            self.redirect("/details?id=" + game.key.urlsafe())
        else:
            self.redirect("/")

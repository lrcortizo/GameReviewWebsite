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

class RemoveCommentHandler(webapp2.RequestHandler):
    def get(self):

        # Se comprueba que el id del comentario
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=Comment was not found")
            return
        user = users.get_current_user()

        if user != None:

            #Se obtiene el comentario
            try:
                comment = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=Comment key was not found")
                return
            if user.user_id() == comment.user:
                #El comentario se elimina
                comment.key.delete()
                time.sleep(1)
            else:
                self.redirect("/error?msg=You don't have premissions to do this")
                return

            #Redireccion
            game = Game.query(comment.game == Game.key).get()
            self.redirect("/details?id=" + game.key.urlsafe())
        else:
            self.redirect("/")



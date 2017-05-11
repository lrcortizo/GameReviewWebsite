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

class RemoveHandler(webapp2.RequestHandler):
    def get(self):
        #Se comprueba que el id del juego
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=Game was not found")
            return
        user = users.get_current_user()

        if user != None:
            # Se obtiene el id del juego
            try:
                game = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=Game key was not found")
                return
            if user.user_id() == game.user:
                # Borrar todos los comentarios de ese juegp
                comments = Comment.query(Comment.game == game.key)
                for c in comments:
                    c.key.delete()
                    time.sleep(1)

                #Se borra el juego
                game.key.delete()
                time.sleep(1)
            else:
                self.redirect("/error?msg=You don't have premissions to do this")
                return

            self.redirect("/usergames")
        else:
            self.redirect("/")



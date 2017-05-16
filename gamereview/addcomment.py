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

class AddCommentHandler(webapp2.RequestHandler):
    def get(self):

        # Se comprueba que se corresponde con el id de un juego
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
                self.redirect("/error?msg=Game key doesn't exist")
                return

            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "game": game,
            }

            template = JINJA_ENVIRONMENT.get_template("/views/addcomment.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")

    def post(self):

        # Se comprueba que se corresponde con el id de un juego
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=Missing id for modification")
            return

        user = users.get_current_user()

        if user != None:
            #Se obtiene el juego al que corresponde
            try:
                game = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=Game key doesn't exist")
                return


            #Comprobacion campos
            if self.request.get("comment").strip() == "":
                self.redirect("/error?msg=Comment field is empty")
                return
            elif self.request.get("finished").strip() != "yes" and self.request.get("finished").strip() != "no":
                self.redirect("/error?msg=You must to indicate if game is finished or no")
                return
            else:
                try:
                    #Se crea el comentario y se extraen los campos del formulario
                    comment = Comment()
                    comment.game = game.key
                    comment.user = user.user_id()
                    comment.nameUser = user.nickname()
                    comment.comment = self.request.get("comment").strip()
                    comment.numHours = int(self.request.get("hours").strip())
                    if "yes" == self.request.get("finished").strip():
                        comment.finished = True
                    else:
                        comment.finished = False

                    comment.punctuation = int(self.request.get("star"))

                    #Se almacena el comentario
                    comment.put()
                    time.sleep(1)
                except:
                    self.redirect("/error?msg=You must to indicate the punctuation and played hours")
                    return

            self.redirect("/details?id="+game.key.urlsafe())
        else:
            self.redirect("/")

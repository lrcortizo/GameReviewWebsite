from google.appengine.api import users
from google.appengine.ext import ndb


from game import Game
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
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=serie was not found")
            return

        user = users.get_current_user()

        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")
            try:
                game = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=key does not exist")
                return

            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "game": game,
            }

            template = JINJA_ENVIRONMENT.get_template("addcomment.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=missing id for modification")
            return

        user = users.get_current_user()

        if user != None:
            try:
                game = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=key does not exist")
                return

            comment = Comment()
            comment.game = game.id
            comment.user = user.user_id()
            comment.comment = self.request.get("comment").strip()
            comment.numHours = self.request.get("hours").strip()

            if len(comment.comment) < 1:
                self.redirect("/error?msg=" + "Modification aborted: serie's name is mandatory")
                return

            comment.put()
            time.sleep(1)
            self.redirect("/details?id="+game.key.urlsafe())
        else:
            self.redirect("/")

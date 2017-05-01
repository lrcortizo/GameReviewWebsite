from google.appengine.api import users

from game import Game

import webapp2


class AddHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user != None:
            game = Game()
            game.user = user.user_id()
            game.name = "Name"
            game.company = "EA"
            game.web = "www.game.com"
            game.commentary = "commentary"
            game.picture = "https://upload.wikimedia.org/wikipedia/commons/6/66/SMPTE_Color_Bars.svg"
            game.put()
            self.redirect("/update?id=" + game.key.urlsafe())
        else:
            self.redirect("/")

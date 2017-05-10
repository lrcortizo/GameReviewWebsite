#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os

from game import Game
from add import AddHandler
from update import UpdateHandler
from remove import RemoveHandler
from details import DetailsHandler
from usergames import UserGamesHandler
from usercomments import UserCommentsHandler
from addcomment import AddCommentHandler
from updatecomment import UpdateCommentHandler
from removecomment import RemoveCommentHandler
from error import ErrorHandler
from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        # Comprobacion usuario
        if user == None:
            user_name = "Please login"
            access_link = users.create_login_url("/")
            iduser = None
        else:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")
            iduser = user.user_id()

        games = Game.query().order(-Game.date)

        template_values = {
            "user_name": user_name,
            "access_link": access_link,
            "games": games,
            "iduser": iduser,

        }

	template = JINJA_ENVIRONMENT.get_template( "/views/index.html" )
	self.response.write(template.render(template_values));

app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/add", AddHandler),
    ("/update", UpdateHandler),
    ("/remove", RemoveHandler),
    ("/error", ErrorHandler),
    ("/details", DetailsHandler),
    ("/usergames", UserGamesHandler),
    ("/usercomments", UserCommentsHandler),
    ("/addcomment", AddCommentHandler),
    ("/updatecomment", UpdateCommentHandler),
    ("/removecomment", RemoveCommentHandler),
], debug=True)

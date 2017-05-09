import os
import webapp2
import jinja2

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            #Se comprueba que hay msg y se obtiene
            try:
                msg = self.request.GET['msg']
            except:
                msg = None

            template_values = {
                "msg": msg,
                "user_name": user_name,
                "acces_link": access_link,
            }
        else:
            self.redirect("/")

        template = JINJA_ENVIRONMENT.get_template( "/views/error.html" )
        self.response.write(template.render(template_values));

from google.appengine.ext import ndb

class Game(ndb.Model):
	user = ndb.StringProperty(required = True)
	name = ndb.StringProperty(required = True)
	date = ndb.DateProperty(auto_now_add = True)
	company = ndb.StringProperty()
	description = ndb.StringProperty()
	web = ndb.StringProperty()
	picture = ndb.StringProperty()
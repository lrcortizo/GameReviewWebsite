from google.appengine.ext import ndb

class Game(ndb.Model):
	user = ndb.StringProperty(required = True)
	nameUser = ndb.StringProperty(required = True)
	name = ndb.StringProperty(required = True)
	date = ndb.DateProperty(auto_now_add = True)
	company = ndb.StringProperty(required = True)
	description = ndb.StringProperty(required = True)
	web = ndb.StringProperty(required = True)
	picture = ndb.StringProperty(required = True)
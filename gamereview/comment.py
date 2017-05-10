from google.appengine.ext import ndb

class Comment(ndb.Model):
    game = ndb.KeyProperty(required = True)
    user = ndb.StringProperty(required = True)
    nameUser = ndb.StringProperty(required=True)
    numHours = ndb.IntegerProperty(required = True)
    finished = ndb.BooleanProperty(required = True)
    comment = ndb.StringProperty(required = True)
    punctuation = ndb.IntegerProperty(required = True)
    date = ndb.DateProperty(auto_now_add = True)
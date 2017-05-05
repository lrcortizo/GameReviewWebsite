from google.appengine.ext import ndb

class Comment(ndb.Model):
    game = ndb.KeyProperty()
    user = ndb.KeyProperty()
    numHours = ndb.StringProperty()
    finished = ndb.BooleanProperty()
    comment = ndb.StringProperty(required = True)
    punctuation = ndb.IntegerProperty()

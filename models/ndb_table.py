from google.appengine.ext import ndb


# Table for storing messages.
class Message(ndb.Model):
    user = ndb.StringProperty()
    date_updated = ndb.DateTimeProperty(auto_now_add=True)
    message = ndb.TextProperty()
    
    
# Access methods. 

def create_message(user=get_user_email(), message=''):
    """Creates a message, returning the key."""
    new_message = Message(parent=ndb.Key('User', user))
    new_message.user = user
    new_message.message = message
    key = new_message.put()
    logger.info("Created a new message with key: %r" % key)
    return key

class Profile(ndb.Model):
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    email = ndb.StringProperty()
    height = ndb.IntegerProperty()
    weight = ndb.IntegerProperty()

def create_profile(user=get_user_email(), name = '', address='', height = 0, weight = 0):
    """Creates a message, returning the key."""
    new_profile = Profile(parent=ndb.Key('User', user))
    new_profile.name = name
    new_profile.email = user
    new_profile.address = address
    new_profile.height = height
    new_profile.weight = weight
    key = new_profile.put()
    logger.info("Created a new profile with key: %r" % key)
    return key    
	
class WorkoutSession(ndb.Model):
    email = ndb.StringProperty()
    r_c = ndb.StringProperty()
    row = ndb.IntegerProperty()
    col = ndb.IntegerProperty()
    minutes = ndb.IntegerProperty()
	
def create_WorkoutSession(user=get_user_email(), r_c = '',row=0, col=0, minutes=None):
    """Creates a message, returning the key."""
    new_WorkoutSession = WorkoutSession(parent=ndb.Key('User', user))
    new_WorkoutSession.email = user
    new_WorkoutSession.r_c = r_c	
    new_WorkoutSession.row = row
    new_WorkoutSession.col = col
    new_WorkoutSession.minutes = minutes
    key = new_WorkoutSession.put()
    logger.info("Created a new workout session with key: %r" % key)
    return key 
	




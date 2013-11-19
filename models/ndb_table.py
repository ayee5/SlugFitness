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

class Goal(ndb.Model):
    email = ndb.StringProperty()
    min = ndb.IntegerProperty()	

def create_goal(user=get_user_email(), min = 400):
    """Creates a message, returning the key."""
    new_goal = Goal(parent=ndb.Key('User', user))
    new_goal.email = user
    new_goal.min = min
    key = new_goal.put()
    logger.info("Created a new goal with key: %r" % key)
    return key

#######################################################
class Event(ndb.Model):
    title = ndb.StringProperty()
    email = ndb.StringProperty()
    event = ndb.TextProperty()
    date = ndb.DateTimeProperty()
    join = ndb.StringProperty()

def create_event(user=get_user_email(), title = '', event='', date = ''):
    """Creates a message, returning the key."""
    new_event = Event(parent=ndb.Key('User', user))
    new_event.title = title
    new_event.email = user
    new_event.event = event
    new_event.date = date
    new_event.join = ""
    key = new_event.put()
    logger.info("Created a new event with key: %r" % key)
    return key     

class Join(ndb.Model):
    keys = ndb.StringProperty()
    title = ndb.StringProperty()
    email = ndb.StringProperty()

def create_join(user=get_user_email(), title = '', keys = ''):
    """Creates a message, returning the key."""
    new_join = Join(parent=ndb.Key('User', user))
    new_join.keys = keys 
    new_join.title = title
    new_join.email = user
    key = new_join.put()
    logger.info("Joined a new event with key: %r" % key)
    return key         

class Comment(ndb.Model):
    keys = ndb.StringProperty()
    title = ndb.StringProperty()
    email = ndb.StringProperty()
    comment = ndb.TextProperty()
    time = ndb.StringProperty()

def create_comment(user=get_user_email(), title = '', comment = '', time = '', keys = ''):
    """Creates a message, returning the key."""
    new_comment = Comment(parent=ndb.Key('User', user))
    new_comment.title = title
    new_comment.email = user
    new_comment.comment = comment
    new_comment.time = time
    new_comment.keys = keys
    key = new_comment.put()
    logger.info("Joined a new event with key: %r" % key)
    return key      

class Trainer(ndb.Model):
    email = ndb.StringProperty()
    information = ndb.TextProperty()
    name = ndb.StringProperty()

def create_trainer(email = '', name = '', information = ''):
    """Creates a message, returning the key."""
    new_trainer = Trainer(parent=ndb.Key('User', user))
    new_trainer.email = user
    new_trainer.name = name
    new_trainer.information = information
    key = new_trainer.put()
    logger.info("Joined a new event with key: %r" % key)
    return key
	




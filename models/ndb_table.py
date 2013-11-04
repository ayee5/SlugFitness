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

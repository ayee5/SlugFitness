# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
def home():
    return dict()

def index():
    """Creates a new message."""
    form = SQLFORM.factory(
        Field('message', 'text')
        )
    if form.process().accepted:
        create_message(message=form.vars.message)
        session.flash = T('Message created')
        redirect(URL('default', 'index'))
    return dict(form=form)

def profile():    
    form = SQLFORM.factory(
        Field('name', 'string'),
        Field('address', 'string'),
        Field('weight', 'integer'),
        Field('height', 'integer'),        
        )
    if form.process().accepted:
        create_profile(name=form.vars.name, address=form.vars.address, weight=form.vars.weight, height=form.vars.height)    
        session.flash = T('Profile created')        
        redirect(URL('default', 'Profile_page'))        
    return dict(form = form)
    
def Profile_page():
	s = get_user_email()
	key = ndb.Key(Profile, s)
	
   
	r = Profile.query()
	myusers = r.fetch(20)
	#myusers = r.fetch(20, projection=[Profile.name])
	
	return dict(myusers=myusers, r=r)
   #return dict(s=s, r=r, myusers=myusers)    
   

def spreadsheet():
	
   return dict()
  
   
   
def event():

   return dict()       

    
def learn():
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

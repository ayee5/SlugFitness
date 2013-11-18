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

@auth.requires_login()
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
       # redirect(URL('default', 'Profile_page'))        
    return dict(form = form)

@auth.requires_login() 	
def Profile_page():
    s = get_user_email()
    key = ndb.Key(Profile, s)

    r = Profile.query()
    myusers = r.fetch(20)

    test = WorkoutSession.query(WorkoutSession.email == "sd")
    nouser = test.fetch(1)
    myt = ""
    testemail = ""
    for j in nouser:
	    testemail = j.email
    if testemail == s:
	    myt = "true"
    else:
	    myt = "false"
    return dict(myusers=myusers, r=r, myt=myt)


#update specified cell in spreadsheet    
def update():
    ##values received from post call
    val = request.vars.values()[1]
    id = request.vars.values()[0]

    ##query ndb for key of specified cell
    curruser = get_user_email()
    quy = WorkoutSession.query()
    quy = quy.filter(WorkoutSession.email==curruser)
    quy = quy.filter(WorkoutSession.r_c == id)
    singleEntry = quy.fetch(1)

    ##Stud is now key. Update minutes
    for u in singleEntry:
	    u.key
    stud = u
    stud.minutes = int(val)
    stud.put()
    return str("s")

#load spreadsheet
@auth.requires_login()
def spreadsheet():
    curruser = get_user_email()
    test = WorkoutSession.query(WorkoutSession.email == curruser)
    nouser = test.fetch(1)
    testemail = ""
    for j in nouser:
        testemail = j.email

    ##declare 2d list to hold workout data
    datalist = []	
    for a in xrange(7):
        datalist.append([])

    ##check if current user has a spreadsheet
    if testemail == curruser:
        r = WorkoutSession.query(WorkoutSession.email == curruser).order(WorkoutSession.r_c)
        work = r.fetch(49)
        for x in work:  #initialize datalist with the query (has spreadsheet)
            datalist[x.row].append(x.minutes)
        return dict(datalist=datalist)
    else:
        for rr in xrange(7):  # initialize datalist with all 0 (has no spreadsheet)
            for cc in xrange(7):
                create_WorkoutSession(r_c=`rr`+`cc`, row=rr, col=cc, minutes=0)
                datalist[rr].append(0)
        return dict(datalist=datalist)

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

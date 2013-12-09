# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

import time

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
def log():
    session.flash = T('You are logged in')
    redirect(URL('default', 'home'))
    return dict()	
	
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

#update goal on spreadsheet    
def updateGoal():
	##values received from post call
    val = request.vars.values()[0]

    ##query ndb for goal of current user
    curruser = get_user_email()
    quy = Goal.query()
    quy = quy.filter(Goal.email==curruser)
    singleEntry = quy.fetch(1)

    ##Stud is now key. Update goal
    for u in singleEntry:
        u.key
    stud = u
    stud.min = int(val)
    stud.put()
    return str(id)


#update specified cell in spreadsheet    
def updateInput():
    ##values received from post call
    val = request.vars.value
    id = request.vars.id

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
    return str(val)

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

    mygoal = 400
    ##check if current user has a spreadsheet
    if testemail == curruser:
        r = WorkoutSession.query(WorkoutSession.email == curruser).order(WorkoutSession.r_c)
        work = r.fetch(49)
        for x in work:  #initialize datalist with the query (has spreadsheet)
            datalist[x.row].append(x.minutes)
        
        go = Goal.query(Goal.email == curruser)
        curr_goal = go.fetch(1)
        for x in curr_goal:  #initialize datalist with the query (has spreadsheet)
            mygoal = x.min 
        return dict(datalist=datalist, mygoal=mygoal, curruser=curruser)
    else:
        create_goal(min = 400)
        for rr in xrange(7):  # initialize datalist with all 0 (has no spreadsheet)
            for cc in xrange(7):
                create_WorkoutSession(r_c=`rr`+`cc`, row=rr, col=cc, minutes=0)
                datalist[rr].append(0)
        return dict(datalist=datalist, mygoal=mygoal, curruser=curruser)

@auth.requires_login()	        
def event():
    form = SQLFORM.factory(
        Field('title', 'string'),
        Field('event', 'text'),
        Field('date', 'datetime'),       
        )
    if form.process(onvalidation=check).accepted:
        create_event(title=form.vars.title, event=form.vars.event, date=form.vars.date)    

        session.flash = T('Event created')        
        redirect(URL('default', 'login'))     
    return dict(form=form)        
    
def mycal():
   flag = 1
   s = get_user_email()
   # key1 = Profile.get_by_id()
  
  # print key1
   fake = ""
   fake = Profile.query(Profile.email == "non").fetch(1)
   print fake   
  
   if str(fake) == "[]":
      print "fake is empty"
  
   check = Profile.query(Profile.email == get_user_email()).fetch(1)
   strcheck = str(check)
   
   if strcheck == "[]":
      flag = 0
   temp = Profile.query().fetch(projection=["name"])
   event = Event.query().fetch(100)
   join = Join.query(Join.email == s).fetch(100)
   
   return dict(s=s, check=check, temp = temp, flag = flag, event = event, join = join)
	
def learn():
    return dict()
    
@auth.requires_login()	
def listevent():
    flag = 1;
    event = Event.query().fetch(100)
    join = Join.query(Join.email == get_user_email()).fetch(100)
    return dict(event = event, join = join, flag = flag)

def join():
   id = request.args(0);
   title = ""
   event = Event.query().fetch()
   for x in event:
        if str(x.key.id()) == id:
           title = x.title   
   create_join(title=title)       
   redirect(URL('default', 'login'))

   return dict(event = event, join = join, flag = flag)    

   
def view():
   flag  = 0
   id = request.args(0)
   print id
   found = ""
   event = Event.query().fetch()
   for x in event:
        if str(x.key.id()) == id:
           found = x.title
           print found 
   
   event = Event.query(Event.title == found).fetch(1)    
   print event
   join = Join.query(Join.title == found).fetch()
   form = SQLFORM.factory(
        Field('comment', 'text'),       
        )
   if form.process().accepted:
        localtime= time.localtime()
        timeString = time.strftime(" %b %d, %Y at %I:%M %p %I:%M:%S", localtime)
        create_comment(title = found, comment=form.vars.comment, time = timeString)    
        session.flash = T('Added in new comment')
        flag = 1         
        
   if flag == 1:
        redirect(URL('default', 'listevent'))
   
   comment = Comment.query(Comment.title == found).order(Comment.title, Comment.time).fetch()    
   return dict(event = event, join = join, form = form, comment = comment, flag = flag)

def editprofile():
    form = SQLFORM.factory(
        Field('name', 'string'),
        Field('address', 'string'),
        Field('weight', 'integer'),
        Field('height', 'integer'),        
        )
    if form.process().accepted:
       # hold = create_profile(name=form.vars.name, address=form.vars.address, weight=form.vars.weight, height=form.vars.height)    
        
        person = Profile.query(Profile.email == get_user_email()).fetch(1)
        for x in person:
           hold = x.key
        temp = hold.get()
        temp.name = form.vars.name
        temp.address = form.vars.address
        temp.weight = form.vars.weight
        temp.height = form.vars.height
        temp.put()
                
        
        session.flash = T('Edited the profile')        
        redirect(URL('default', 'login'))      
    return dict(form = form)   

def editevent():
    id = request.args(0)
    title = ""

    allevent = Event.query().fetch()
    for a in allevent:
        if str(a.key.id()) == id:
           title = a.title
   
    form = SQLFORM.factory(
        Field('title', 'string'),
        Field('event', 'text'),
        Field('date', 'datetime'),            
        )
    if form.process(onvalidation=check).accepted:
       # hold = create_profile(name=form.vars.name, address=form.vars.address, weight=form.vars.weight, height=form.vars.height)    
        
        event = Event.query(Event.title == title).fetch(1)
        join = Join.query(Event.title == title).fetch()
        comment = Comment.query(Comment.title == title).fetch()
        for x in event:
           hold = x.key        
        temp = hold.get()
        temp.title = form.vars.title
        temp.event = form.vars.event
        temp.date = form.vars.date
        temp.put()
        
        for y in join:
           store = y.key
           change = store.get()
           change.title = form.vars.title
           change.put()           
                
        for z in comment:
           store = z.key
           change = store.get()
           change.title = form.vars.title
           change.put()
        
        session.flash = T('Edited the event')        
        redirect(URL('default', 'login'))      
    return dict(form = form)   

def trainer():
    rows = Trainer.query().fetch()              
    return dict(rows = rows)
    
def result():
   id = request.args(0)
   empty = ""
   found = ""
   trainer = Trainer.query().fetch()
   if id is None:
      empty = "There is no result"
   
   for x in trainer:
      if str(x.key.id()) == id:
         found = x.name
         print found 
   
   trainer = Trainer.query(Trainer.name == found).fetch(1)    

   return dict(empty = empty, trainer = trainer, id = id)    

def test():
   temp = ""
   search = request.vars.search
   print search
   
   trainer = Trainer.query(Trainer.name == search).fetch()
   for x in trainer:
      temp = x.key.id()
         
   return str(temp)   

@auth.requires_login() 
def login():
   flag = 1
   s = get_user_email()
   # key1 = Profile.get_by_id()
  
  # print key1
   fake = ""
   fake = Profile.query(Profile.email == "non").fetch(1)
   print fake   
  
   if str(fake) == "[]":
      print "fake is empty"
  
   check = Profile.query(Profile.email == get_user_email()).fetch(1)
   strcheck = str(check)
   
   if strcheck == "[]":
      flag = 0
   temp = Profile.query().fetch(projection=["name"])
   event = Event.query().fetch(100)
   join = Join.query(Join.email == s).fetch(100)
   
   return dict(s=s, check=check, temp = temp, flag = flag, event = event, join = join)

def check(form):   
   u = form.vars.title
   y = form.vars.date   
   if u == "":
      form.errors.title = T("Please enter a title")
   if y is None:
      form.errors.date = T("Please enter a date")     

def createtrainer():
    form = SQLFORM.factory(
        Field('name', 'string'),
        Field('information', 'text'),
        Field('phrase', 'string'),            
        )
    if form.process().accepted:
        create_trainer(name=form.vars.name, information=form.vars.information, phrase=form.vars.phrase)    
        session.flash = T('Trainer created')        
        redirect(URL('default', 'trainer'))        
    return dict(form = form)    

def createclasses():
    form = SQLFORM.factory(
        Field('name', 'string'),
        Field('description', 'text'),
        Field('instructor', 'string'),  
        Field('classtime', 'datetime'),                    
        )
    if form.process().accepted:
        create_classes(name=form.vars.name, description=form.vars.description, instructor=form.vars.instructor, classtime = form.vars.classtime)    
        session.flash = T('classes created')        
        redirect(URL('default', 'trainer'))        
    return dict(form = form)       
   
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

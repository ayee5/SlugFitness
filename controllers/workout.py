try:
    from gluon.contrib.spreadsheet import Sheet
except:
    exec('from applications.%s.modules.sheet import Sheet' % request.application)

def spreadsheet():
	if request.args:
        sheet = Sheet.loads(session.psheet)
        jquery=sheet.process(request)
        session.psheet=sheet.dumps()
        return jquery
    else:
        sheet=Sheet(7,7,URL(r=request))
        #sheet = Sheet.loads(session.psheet)
        #sheet.cell('r0c3' % i,value='=r0c0+r0c1+r0c2',readonly=True)
        session.psheet = sheet.dumps()
        day = ['Monday', 'Tuesday' , 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return dict(sheet=sheet, day=day)


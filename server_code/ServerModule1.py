import anvil.secrets
import anvil.stripe
import anvil.files
from anvil.files import data_files
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def getEmails(user):
  r=''
  for i in app_tables.table_1.search(Name=user):
    r+=anvil.secrets.decrypt_with_key('jlsr',i["Content"])+' from '+i['Sender']+'\n'
  for i in app_tables.table_1.search(Sender=user):
    r+=anvil.secrets.decrypt_with_key('jlsr',i["Content"])+' to '+i['Name']+'\n'
  return r

@anvil.server.callable
def sendEmail(user,recipient,c):
  for i in recipient:
    app_tables.table_1.add_row(Content=anvil.secrets.encrypt_with_key('jlsr',c),Sender=user,Name=i)

@anvil.server.callable
def addFile(user,file):
  app_tables.drive.add_row(User=user,File=file,Name=file.name)

@anvil.server.callable
def getFiles(user):
  x=[]
  for i in app_tables.drive.search(User=user):
    x.append(i['File'])
  return x

@anvil.server.callable
def deleteFile(filename):
  for i in app_tables.drive.search(Name=filename):
    i.delete()

@anvil.server.callable
def visit():
  while len(app_tables.table_1.search())>500:
    app_tables.table_1.search()[0].delete()

@anvil.server.route("/mail")
def mail():
  return anvil.server.FormResponse('Form1')

@anvil.server.route('/maps')
def maps():
  return anvil.server.FormResponse('Maps')

@anvil.server.route('/feed')
def feed():
  res=anvil.server.HttpResponse(302,"Redirecting to feedback form...")
  res.headers['Location']='https://flat-tempting-hedgehog.anvil.app'
  return res

@anvil.server.route('/auth/user/:s')
def auth(s):
  text=anvil.users.get_user(allow_remembered=True)['email']
  x=anvil.users.get_user(allow_remembered=True)['Services']
  if x:
    if s in x.split(','):
      return text
  r=anvil.server.HttpResponse(302,"Redirecting to allow...")
  r.headers['Location']='https://fast-small-grison.anvil.app/allow/'+s
  return r


@anvil.server.route('/allow/:service')
def allows(service):
  t=anvil.server.AppResponder(data={'service':service})
  return t.load_form('Allow')

@anvil.server.callable
def allow(text):
  if not anvil.users.get_user(allow_remembered=True)['Services']:
    anvil.users.get_user(allow_remembered=True)['Services']=text
  else:
    anvil.users.get_user(allow_remembered=True)['Services']+=','+text

@anvil.server.callable
def update(text):
  anvil.users.get_user(allow_remembered=True)['Services']=text

@anvil.server.route('/services')
def manage():
  return anvil.server.FormResponse('ManageServices')
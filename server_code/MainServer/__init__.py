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
  u=app_tables.users.get(email=user)
  if u['emails']:
    for i in u['emails']:
      r+=anvil.secrets.decrypt_with_key('jlsr',i["Content"])+' from '+i['Sender']+'\n'
  return r

@anvil.server.callable
def sendEmail(user,recipient,c):
  for i in recipient:
    #app_tables.table_1.add_row(Content=anvil.secrets.encrypt_with_key('jlsr',c),Sender=user,Name=i)
    x=app_tables.users.get(email=i)
    if not x:
      return
    else:
      x=x['emails']
    if not x:
      y=[]
    else:
      y=x
    y.append({'Content':anvil.secrets.encrypt_with_key('jlsr',c),'Sender':user})
    app_tables.users.get(email=i)['emails']=y

@anvil.server.callable
def delemail(id):
  x=anvil.users.get_user(allow_remembered=True)
  if x['emails']:
    y=x['emails']
    del y[int(id)-1]
    anvil.users.get_user(allow_remembered=True)['emails']=y

@anvil.server.background_task
def videotask(image):
  anvil.users.get_user()["Image"]=image

@anvil.server.callable
def video(image):
  user = anvil.users.get_user()
  if user:
    # Save the latest video chunk to the user's row
    user["Image"] = image

@anvil.server.callable
def getmeet():
  user = anvil.users.get_user()
  if not user or not user['Meet_Name']:
    return []

    # Get all users in the same meeting except yourself
  others = app_tables.users.search(
    Meet_Name=user['Meet_Name']
  )

  # Return their latest "Image" (video segment)
  return [r['Image'] for r in others if r != user and r['Image']]

@anvil.server.callable
def setmeet(meet_id):
  user = anvil.users.get_user()
  if user:
    user["Meet_Name"] = meet_id

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
def profile(f):
  anvil.users.get_user(allow_remembered=True)['Profile']=f

@anvil.server.callable
def pic():
  return anvil.users.get_user()["Profile"]

@anvil.server.callable
def visit():
  while len(app_tables.table_1.search())>500:
    app_tables.table_1.search()[0].delete()

@anvil.server.route("/mail")
def mail():
  return anvil.server.FormResponse('Form1')

@anvil.server.route('/meet/:id')
def meet(id):
  setmeet(id)
  return anvil.server.FormResponse('Meet')

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

@anvil.server.route('/apps')
def apps():
  return anvil.server.FormResponse('Apps')

@anvil.server.route('/settings')
def settings():
  return anvil.server.FormResponse('Settings')

@anvil.server.route('/send/:p')
def send(p):
  t=anvil.server.AppResponder(data={'contact':p})
  return t.load_form('Form1')
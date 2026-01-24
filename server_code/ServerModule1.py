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
import io
import csv
import anvil.media

@anvil.server.callable
def append_to_media(existing_media, new_text):
  # 1. Get existing content as bytes
  old_bytes = existing_media.get_bytes()

  # 2. Convert new content to bytes (with a newline if needed)
  new_bytes = f"\n{new_text}".encode('utf-8')

  # 3. Concatenate and create a new BlobMedia object
  updated_media = anvil.BlobMedia(
    content_type=existing_media.content_type,
    content=old_bytes + new_bytes,
    name=existing_media.name
  )

  return updated_media


@anvil.server.callable
def search_csv_media(csv_media, search_column, search_value):
  # Convert Anvil Media object to a file-like stream
  try:
    csv_bytes = csv_media.get_bytes()
  except:
    return []
  csv_string = csv_bytes.decode('utf-8')
  csv_file = io.StringIO(csv_string)
  x=[]
  reader = csv.DictReader(csv_file)
  for row in reader:
    if row.get(search_column) == search_value:
      x.append(dict(row))  # Return the first matching row as a dictionary

  return x

@anvil.server.callable
def email_csv():
  """
  Retrieves data table rows and serializes them into a CSV file 
  returned as an Anvil Media object.
  """
  # 1. Retrieve data
  rows = app_tables.table_1.search()

  # 2. Convert rows to a list of dictionaries (simple serialization)
  data_list = [dict(row) for row in rows]

  # 3. Generate file content in memory using io.BytesIO
  output = io.BytesIO()
  writer = csv.DictWriter(output, fieldnames=data_list[0].keys())
  writer.writeheader()
  writer.writerows(data_list)

  # 4. Create an Anvil Media object
  media_object = anvil.BlobMedia(
    content_type="text/csv", 
    content=output.getvalue(), 
    name="exported_data.csv"
  )

  # 5. Return the Media object
  return append_to_media(app_tables.export.search(Name='main')[0]['File'],media_object)


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
  x=app_tables.export.search(Name='main')[0]['File']
  for i in search_csv_media(x,'Name',user):
    r+=anvil.secrets.decrypt_with_key('jlsr',i["Content"])+' from '+i['Sender']+'\n'
  for i in search_csv_media(x,'Sender',user):
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
  if s in anvil.users.get_user(allow_remembered=True)['Services'].split(','):
    return text
  else:
    return ""


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

@anvil.server.background_task('export')
def export():
  x=app_tables.export.search(Name='main')
  for i in x:
    if True:
      i['File']=email_csv()
    else:
      i['File']=anvil.BlobMedia('text/plain',"".encode('utf-8'))
      return
  x=app_tables.table_1.search()
  for i in x:
    i.delete()

@anvil.server.callable
def v2():
  anvil.server.launch_background_task('export')
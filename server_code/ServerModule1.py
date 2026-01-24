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

# --- Media Helper Functions ---

@anvil.server.callable
def append_to_media(existing_media, new_media_to_append):
  """
    Takes an existing Media object and appends the content of a second 
    Media object to it.
    """
  # 1. Get existing content
  old_bytes = existing_media.get_bytes()

  # 2. Get new content
  new_bytes = new_media_to_append.get_bytes()

  # 3. Concatenate (adding a newline to separate CSV records if necessary)
  updated_content = old_bytes + b"\n" + new_bytes

  # 4. Create and return a new BlobMedia object
  return anvil.BlobMedia(
    content_type=existing_media.content_type,
    content=updated_content,
    name=existing_media.name
  )

@anvil.server.callable
def search_csv_media(csv_media, search_column, search_value):
  """
    Reads a Media object as a CSV without saving to disk.
    """
  try:
    csv_bytes = csv_media.get_bytes()
    # Decode bytes to string for StringIO
    csv_string = csv_bytes.decode('utf-8')
    csv_file = io.StringIO(csv_string)

    results = []
    reader = csv.DictReader(csv_file)
    for row in reader:
      if row.get(search_column) == search_value:
        results.append(dict(row))
    return results
  except Exception as e:
    print(f"Error reading CSV media: {e}")
    return []

# --- Email and Data Management ---

@anvil.server.callable
def email_csv():
  """
    Retrieves data table rows and serializes them into a CSV Media object.
    """
  rows = app_tables.table_1.search()
  if not rows:
    return None

    # Convert rows to list of dicts
  data_list = [dict(row) for row in rows]

  # Use StringIO to build the CSV string
  output = io.StringIO()
  writer = csv.DictWriter(output, fieldnames=data_list[0].keys())
  writer.writeheader()
  writer.writerows(data_list)

  # Convert string to bytes for BlobMedia
  media_object = anvil.BlobMedia(
    content_type="text/csv", 
    content=output.getvalue().encode('utf-8'), 
    name="exported_data.csv"
  )

  # Get the master file and append this new batch to it
  master_row = app_tables.export.search(Name='main')[0]
  return append_to_media(master_row['File'], media_object)

@anvil.server.callable
def getEmails(user):
  r = ''
  x = app_tables.export.search(Name='main')[0]['File']
  # Search where user is the Recipient (Name)
  for i in search_csv_media(x, 'Name', user):
    content = anvil.secrets.decrypt_with_key('jlsr', i["Content"])
    r += f"{content} from {i['Sender']}\n"
    # Search where user is the Sender
  for i in search_csv_media(x, 'Sender', user):
    content = anvil.secrets.decrypt_with_key('jlsr', i["Content"])
    r += f"{content} to {i['Name']}\n"
  return r

@anvil.server.callable
def sendEmail(user, recipient, c):
  for i in recipient:
    app_tables.table_1.add_row(
      Content=anvil.secrets.encrypt_with_key('jlsr', c),
      Sender=user,
      Name=i
    )

# --- File Management ---

@anvil.server.callable
def addFile(user, file):
  app_tables.drive.add_row(User=user, File=file, Name=file.name)

@anvil.server.callable
def getFiles(user):
  return [i['File'] for i in app_tables.drive.search(User=user)]

@anvil.server.callable
def deleteFile(filename):
  for i in app_tables.drive.search(Name=filename):
    i.delete()

# --- Housekeeping and Routes ---

@anvil.server.callable
def visit():
  """Keep table size manageable."""
  rows = app_tables.table_1.search()
  while len(rows) > 500:
    rows[0].delete()
    rows = app_tables.table_1.search()

@anvil.server.callable
def v2():
  """Archive current table to CSV and clear table."""
  main_rows = app_tables.export.search(Name='main')
  for row in main_rows:
    new_file = email_csv()
    if new_file:
      row['File'] = new_file

    # Clear table after archiving
  for i in app_tables.table_1.search():
    i.delete()

# --- HTTP Routes ---

@anvil.server.route("/mail")
def mail():
  return anvil.server.FormResponse('Form1')

@anvil.server.route('/maps')
def maps():
  return anvil.server.FormResponse('Maps')

@anvil.server.route('/feed')
def feed():
  res = anvil.server.HttpResponse(302)
  res.headers['Location'] = 'https://flat-tempting-hedgehog.anvil.app'
  return res

@anvil.server.route('/auth/user/:s')
def auth(s):
  user = anvil.users.get_user(allow_remembered=True)
  if not user: return ""
  services = user['Services'].split(',') if user['Services'] else []
  return user['email'] if s in services else ""

@anvil.server.route('/allow/:service')
def allows(service):
  t = anvil.server.AppResponder(data={'service': service})
  return t.load_form('Allow')

@anvil.server.callable
def allow(text):
  user = anvil.users.get_user(allow_remembered=True)
  if not user['Services']:
    user['Services'] = text
  else:
    user['Services'] += ',' + text

@anvil.server.callable
def update(text):
  user = anvil.users.get_user(allow_remembered=True)
  user['Services'] = text

@anvil.server.route('/services')
def manage():
  return anvil.server.FormResponse('ManageServices')

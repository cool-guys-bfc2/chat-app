import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import zipfile
import io

@anvil.server.callable
def upload(f):
  x=anvil.users.get_user()['Files']
  if not x:
    x={}
  x[f.name]=f.get_bytes()
  anvil.users.get_user()['Files']=x


@anvil.server.callable
def delete_file(f):
  x=anvil.users.get_user()['Files']
  try:
    del x[f]
  except:
    pass
  anvil.users.get_user()['Files']=x

@anvil.server.callable
def get_my_files():
  x=anvil.users.get_user()['Files']
  if not x:
    x={}
    anvil.users.get_user()['Files']={}
  y=[{'file':anvil.BlobMedia(content=x[i], name=i),'filename':i} for i in x]
  return y

@anvil.server.callable
def get_user_zip():
  user = anvil.users.get_user()
  files = user["Files"]

  if not files:
    files={}
    anvil.users.get_user()["Files"]=files

    # Create ZIP in memory
  zip_buffer = io.BytesIO()
  with zipfile.ZipFile(zip_buffer, 'w') as out_zip:
    for row in files:
      # Write the bytes of each stored media object into the zip
      out_zip.writestr(row, files[row])

  zip_buffer.seek(0)
  x=anvil.BlobMedia("application/zip", zip_buffer.read(), name="my_files.zip")
  return x

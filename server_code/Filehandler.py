import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import zipfile
import io

@anvil.server.callable
def get_user_zip():
  user = anvil.users.get_user()
  files = user["Files"]

  if not files:
    

    # Create ZIP in memory
  zip_buffer = io.BytesIO()
  with zipfile.ZipFile(zip_buffer, 'w') as out_zip:
    for row in files:
      # Write the bytes of each stored media object into the zip
      out_zip.writestr(row, files[row].get_bytes())

  zip_buffer.seek(0)
  return anvil.BlobMedia("application/zip", zip_buffer.read(), name="my_files.zip")

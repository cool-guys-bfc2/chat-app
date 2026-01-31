from ._anvil_designer import FilesTemplate
from anvil import *
import anvil.server
import m3.components as m3
import stripe.checkout
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media

class Files(FilesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_file_buttons()

    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    x=anvil.server.call('get_user_zip')
    anvil.media.download(x)

  @handle("file_loader_1", "change")
  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    anvil.server.call('upload',file)
  
  def refresh_file_buttons(self):
    # Clear existing buttons

    # Fetch files from server
    user_files = anvil.server.call('get_my_files')

    for row in user_files:
      # Create a new Button element
      btn = Button(text=row['filename'], role='secondary-color')
      btn2=Button(text="Delete")
      # Use a lambda or a closure to handle the download
      btn.set_event_handler('click', lambda sender, r=row, **event_args: self.download_file(r))
      btn2.set_event_handler('click', lambda sender, r=row, **event_args: self.delete_file(r))

      # Add the button element to the container
      self.layout.add_component(btn)
      self.layout.add_component(btn2)

  def download_file(self, file_row):
    anvil.media.download(file_row['file'])
  def delete_file(self,r):
    anvil.server.call('delete',r['filename'])

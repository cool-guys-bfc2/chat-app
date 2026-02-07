from ._anvil_designer import FileTemplate
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


class File(FileTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    try:
      self.load()
    except:
      pass
    # Any code you write here will run before the form opens.
  def load(self):
    it=[]
    f=anvil.users.get_user()['Files']
    if not f:
      f={}
      anvil.users.get_user()['Files']=f
    for i in f:
      c=anvil.server.call_s('readf',i)
      it.append({'content':c,'name':i})
    self.repeating_panel_1.items=it
  @handle("file_loader_1", "change")
  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    c=confirm('Upload file?')
    if c:
      try:
        anvil.server.call_s('writef',file.name,file.get_bytes().decode('utf-8'))
      except:
      # 1. Strip the header if it's a full Data URI (e.g., 'data:image/png;base64,xxxx')
        anvil.server.call_s('writef',file.name,anvil.js.window.atob(file.get_bytes().decode('latin-1')))

    # 4. Create an Anvil Media object
    # This can be assigned to an Image component's .source property

  @handle("timer_1", "tick")
  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    with anvil.server.no_loading_indicator:
      self.load()

from ._anvil_designer import DocTemplate
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


class Doc(DocTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load()
  def load(self):
    x=anvil.server.call_s('getdocs')
    it=[]
    for k in x:
      v=x[k]
      it.append({'name':k,'content':v})
    self.repeating_panel_1.items=it
    # Any code you write here will run before the form opens.

  @handle("file_loader_1", "change")
  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    c=confirm('Upload file?')
    if c:
      try:
        x=anvil.server.call_s('getdocs')
        c=file.get_bytes().dedode('utf-8')
        x[file.name]=''
        anvil.server.call_s('setdocs',x)
      except:
        alert('Something went wrong. Please try again.')
      self.load()

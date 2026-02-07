from ._anvil_designer import PhotosTemplate
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


class Photos(PhotosTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load()
    # Any code you write here will run before the form opens.
  @handle("file_loader_1", "change")
  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if not anvil.users.get_user()['img']:
      anvil.users.get_user()['img']={}
    x=anvil.users.get_user()['img']
    x[file.name]=anvil.server.call('image_to_rgba_list',file)
    anvil.users.get_user()['img']=x
    self.load()
  def load(self):
    it=[]
    x=anvil.users.get_user()['img']
    if not x:
      x={}
      anvil.users.get_user()['img']=x
    for k in x:
      v=x[k]
      i=anvil.server.call_s('rgba_list_to_media',v)
      it.append({'src':i})
    self.repeating_panel_1.items=it

from ._anvil_designer import DriveTemplate
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

class Drive(DriveTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load()
    # Any code you write here will run before the form opens.
  def upload(self,f):
    x=anvil.users.get_user()['Files']
    x[f.name]={
      'content':f.get_bytes().decode('utf-8'),
      'size':f.length
    }
    anvil.users.get_user()['Files']=x
  def load(self):
    self.files.items=[]
    x=anvil.users.get_user()
    if x['Files']:
      y=x['Files']
    else:
      y={}
      anvil.users.get_user()['Files']=y
    for i in y:
      t={}
      v=y[i]
      t['content']=v['content']
      t['name']=i
      t['size']=v['size']
      self.files.items.append(t)

  @handle("file_loader_1", "change")
  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.upload(file)
    self.load()

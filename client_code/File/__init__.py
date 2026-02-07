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
    
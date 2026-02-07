from ._anvil_designer import ItemTemplate1Template
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
import anvil.js


class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    try:
      self.init_components(**properties)
      x=anvil.js.window.btoa(self.item['content'])
      y=anvil.BlobMedia('image/png',x,name=self.item['name'])
      self.image_1.source=y
    except:
      pass
    # Any code you write here will run before the form opens.

  @handle("text_box_1", "pressed_enter")
  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses enter in this component."""
    x=anvil.users.get_user()['Files']
    y=x[self.item['name']]
    try:
      del x[self.item['name']]
    except:
      pass
    self.item['name']=self.text_box_1.text
    x[self.text_box_1.text]=y
    anvil.users.get_user()['Files']=x

  @handle("text_box_1", "change")
  def text_box_1_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.text_box_1_pressed_enter()

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    x=anvil.users.get_user()['Files']
    if confirm('Delete file?'):
      try:
        del x[self.item['name']]
      except:
        pass
      anvil.users.get_user()['Files']=x
    

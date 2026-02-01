from ._anvil_designer import ContactTemplate
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


class Contact(ContactTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    try:
      self.dropdown_menu_1.items=anvil.users.get_user()["contacts"].split(",")
    except:
      anvil.users.get_user()['contacts']=""
    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    x=self.dropdown_menu_1.selected_value
    anvil.js.window.open('https://fast-small-grison.anvil.app/send/'+x)

  @handle("dropdown_menu_1", "change")
  def dropdown_menu_1_change(self, **event_args):
    """This method is called when an item is selected"""
    x=self.dropdown_menu_1.selected_value
    self.image_1.source=anvil.server.call_s('extpic',x)
    try:
      self.text_1.text=app_tables.users.get(email=x)['Name']
    except:
      self.text_1.text=""
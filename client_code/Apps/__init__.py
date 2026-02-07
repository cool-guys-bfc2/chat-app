from ._anvil_designer import AppsTemplate
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

class Apps(AppsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("navigation_link_2", "click")
  def navigation_link_2_click(self, **event_args):
    """This method is called when the component is clicked"""
    pass

  @handle("navigation_link_4", "click")
  def navigation_link_4_click(self, **event_args):
    """This method is called when the component is clicked"""
    pass

  @handle("link_1", "click")
  def link_1_click(self, **event_args):
    """This method is called clicked"""
    pass

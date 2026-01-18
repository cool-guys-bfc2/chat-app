from ._anvil_designer import AllowTemplate
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


class Allow(AllowTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.button_1.text+=anvil.server.startup_data['service']
    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    anvil.server.call('allow',anvil.server.startup_data['service'])
    anvil.alert("Done!")
    anvil.js.window.close()

  @handle("button_2", "click")
  def button_2_click(self, **event_args):
    """This method is called when the component is clicked."""
    anvil.js.window.close()

from ._anvil_designer import ManageServicesTemplate
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


class ManageServices(ManageServicesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.s=anvil.users.get_user(allow_remembered=True)['Services']
    self.text_1.text=self.s
    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    x=self.s.split(',')
    x.remove(self.text_box_1.text)
    self.s=",".join(x)
    anvil.server.call('update',self.s)
    self.text_1.text=self.s
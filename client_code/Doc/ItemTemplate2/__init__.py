from ._anvil_designer import ItemTemplate2Template
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


class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("text_area_1", "change")
  def text_area_1_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    x=anvil.server.call_s('getdocs')
    x[self.item['name']]=self.text_area_1.text
    anvil.server.call_s('setdocs',x)

  @handle("text_box_1", "change")
  def text_box_1_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    x=anvil.server.call_s('getdocs')
    y=x[self.item['name']]
    if self.text_box_1.text not in x:
      try:
        del x[self.item['name']]
      except:
        pass
      x[self.text_box_1.text]=y
    anvil.server.call_s('setdocs',x)
    self.item['name']=self.text_box_1.text

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    x=anvil.server.call_s('getdocs')
    del x[self.item['name']]
    anvil.server.call_s('setdocs',x)

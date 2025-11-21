from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import m3.components as m3


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called clicked"""
    pass
  def load_click(self, **event_args):
    self.text_1.text=anvil.server.call('getEmails',user=self.text_box_1.text)
  def icon_button_1_click(self, **event_args):
    anvil.server.call('sendEmail',user=self.text_box_1.text,c=self.content.text,recipient=[self.recipient.text])

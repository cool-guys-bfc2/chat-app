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
    x=anvil.server.call('getProjects')
    for i in x:
      new_link = Link(text=i, url=x[i])
      self.layout.add_component(new_link)

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called clicked"""
    pass

from ._anvil_designer import SettingsTemplate
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


class Settings(SettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    try:
      self.image_1.source=anvil.server.call_s('pic')
    except:
      pass
    try:
      self.text_box_1.text=anvil.users.get_user()['contacts']
    except:
      pass
  @handle("file_loader_1", "change")
  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    anvil.server.call_s('profile',file)
    self.image_1.source=file

  @handle("text_box_1", "change")
  def text_box_1_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    with anvil.server.no_loading_indicator:
      anvil.users.get_user()["contacts"]=self.text_box_1.text

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    x=self.text_box_1.text
    y=x.split(",")
    if self.text_area_1.text!="":
      y.append(self.text_area_1.text)
    self.text_box_1.text=",".join(y)
    self.text_box_1_change()
    self.text_area_1.text=""

  @handle("button_2", "click")
  def button_2_click(self, **event_args):
    """This method is called when the component is clicked."""
    x=self.text_box_1.text
    y=x.split(',')
    try:
      y.remove(self.text_area_1.text)
    except:
      pass
    self.text_box_1.text=",".join(y)
    self.text_box_1_change()
    self.text_area_1.text=''

  @handle("text_box_2", "change")
  def text_box_2_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    anvil.users.get_user()['Name']=self.text_box_2.text

from ._anvil_designer import Form1Template
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import m3.components as m3
class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.rec=[]
    # Any code you write here will run before the form opens.
  def link_1_click(self, **event_args):
    """This method is called clicked"""
    pass
  def load_click(self, **event_args):
    self.text_box_1.text=anvil.users.get_user(allow_remembered=True)
    self.text_1.text=anvil.server.call('getEmails',user=self.text_box_1.text)
  def icon_button_1_click(self, **event_args):
    self.text_box_1.text=anvil.users.get_user(allow_remembered=True)
    anvil.server.call('sendEmail',user=self.text_box_1.text,c=self.content.text,recipient=self.rec)
    self.rec=[]
    self.text_1.text=anvil.server.call('getEmails',user=self.text_box_1.text)

  def button_2_click(self, **event_args):
    anvil.users.login_with_form(allow_remembered=True,allow_cancel=True)
    self.text_box_1.text=anvil.users.get_user(allow_remembered=True)
    pass

  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    anvil.users.signup_with_form(allow_cancel=True,remember_by_default=True)

  def icon_button_2_click(self, **event_args):
    self.rec.append(self.recipient.text)
    self.text_6.text+=' '+self.recipient.text
    self.recipient.text=''

  def button_3_click(self, **event_args):
    """This method is called when the component is clicked."""
    try:
      del self.rec[len(self.rec)-1]
    except:
      pass
    self.text_6.text=' '.join(self.rec)

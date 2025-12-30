from ._anvil_designer import Form1Template
from anvil import *
import stripe.checkout
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
    self.fileurls={}
    # Any code you write here will run before the form opens.
  def pay(self,amount):
    c=stripe.checkout.charge(amount=amount,currency="USD")
    print(c)
  def link_1_click(self, **event_args):
    """This method is called clicked"""
    pass
  def load_click(self, **event_args):
    self.text_box_1.text=anvil.users.get_user(allow_remembered=True)
    self.text_1.text=anvil.server.call('getEmails',user=self.text_box_1.text)
    files = anvil.server.call('getFiles', user=self.text_box_1.text)
    self.files.text=''
    for f in files:
      x=f.url
      self.files.text+='\n\n'+f.name+': \n\n'+x
      print(x)
      self.fileurls[f.name]=f.url
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

  def button_4_click(self, **event_args):
    """This method is called when the component is clicked."""
    anvil.users.logout(invalidate_client_objects=False)

  def content_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    pass
  def button_5_click(self, **event_args):
    """This method is called when the component is clicked."""
    try:
      anvil.server.call('addFile',user=self.text_box_1.text,file=self.file_loader_1.file)
    except:
      pass

  def button_6_click(self, **event_args):
    """This method is called when the component is clicked."""
    try:
      i=self.delete.text
      anvil.server.call('deleteFile',filename=i)
      del self.fileurls[i]
      files = anvil.server.call('getFiles', user=self.text_box_1.text)
      self.files.text=''
      for f in files:
        x=f.url
        self.files.text+='\n\n'+f.name+': \n\n'+x
        print(x)
        self.fileurls[f.name]=f.url
      self.delete.text=''
      self.error.text='No errors'
    except:
      self.error.text='File does not exist...'

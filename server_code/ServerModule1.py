import anvil.files
from anvil.files import data_files
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def getEmails(user):
  r=''
  for i in app_tables.table_1.search(Name=user):
    r+=i['Content']+' from '+i['Sender']+'\n'
  for i in app_tables.table_1.search(Sender=user):
    r+=i['Content']+' to '+i['Name']+'\n'
  return r

@anvil.server.callable
def sendEmail(user,recipient,c):
  for i in recipient:
    app_tables.table_1.add_row(Content=c,Sender=user,Name=i)
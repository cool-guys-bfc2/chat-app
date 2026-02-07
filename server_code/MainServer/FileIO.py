import anvil.secrets
import anvil.stripe
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
import re

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
def decode(b,uchar=True):
  t=b.decode('windows-1252')
  if uchar:
    return t
  else:
    result = re.sub(r'\\u([0-9a-fA-F]{4})', r'uchar\1', t)
    return result

@anvil.server.callable
def encode(t,text=True):
  result = re.sub(r'uchar([0-9a-fA-F]{4})', r'\\u\1', t)
  if text:
    return result
  else:
    return result.encode('windows-1252')

@anvil.server.callable
def writef(fname,f):
  x=anvil.users.get_user()
  if not x:
    return
  else:
    y=x['Files']
    if not y:
      y={}
    if True:
      v=y
      if fname not in v:
        v[fname]={'content':''}
      v[fname]['content']=decode(f,uchar=isinstance(f,str))
      anvil.users.get_user()['Files']=v

@anvil.server.callable
def readf(fname):
  try:
    return encode(anvil.users.get_user()['Files'][fname]['content'])
  except:
    return None
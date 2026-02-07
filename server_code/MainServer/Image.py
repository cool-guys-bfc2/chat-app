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
import anvil.media
from PIL import Image

@anvil.server.callable
def image_to_rgba_list(media_obj):
  # 1. Open the Media object as an image
  with anvil.media.TempFile(media_obj) as f:
    img = Image.open(f).convert("RGBA")

    # 2. Extract width and height
  width, height = img.size

  # 3. Get raw pixel data as a flat list of (R, G, B, A) tuples
  pixels = list(img.getdata())

  # 4. Reshape into a 2D list: list[rows][columns]
  rgba_2d_list = [pixels[i * width:(i + 1) * width] for i in range(height)]

  return rgba_2d_list

@anvil.server.callable
def rgba_list_to_media(rgba_2d_list):
  # 1. Determine dimensions
  height = len(rgba_2d_list)
  width = len(rgba_2d_list[0])

  # 2. Flatten the 2D list into a single list of tuples
  flat_pixels = [pixel for row in rgba_2d_list for pixel in row]

  # 3. Create a new Image object
  new_img = Image.new("RGBA", (width, height))
  new_img.putdata(flat_pixels)

  # 4. Save to a byte stream and return as Anvil Media
  img_byte_arr = io.BytesIO()
  new_img.save(img_byte_arr, format='PNG')

  return anvil.BlobMedia("image/png", img_byte_arr.getvalue(), name="processed.png")

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

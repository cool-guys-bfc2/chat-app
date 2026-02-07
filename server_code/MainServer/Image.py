import io
import anvil.server
import anvil.media
from PIL import Image

@anvil.server.callable
def image_to_rgba_list(media_obj):
  """Converts an Anvil Media object to a 2D list of (R, G, B, A) tuples."""
  with anvil.media.TempFile(media_obj) as f:
    img = Image.open(f).convert("RGBA")

  width, height = img.size
  # Extracts all pixels as a flat list of tuples
  pixels = list(img.getdata()) 

  # Reshape into a 2D list: [rows][columns]
  return [pixels[i * width:(i + 1) * width] for i in range(height)]

@anvil.server.callable
def rgba_list_to_media(rgba_2d_list):
  """Converts a 2D list of tuples or packed integers back to an Anvil Media object."""
  if not rgba_2d_list or not rgba_2d_list[0]:
    return None

  height = len(rgba_2d_list)
  width = len(rgba_2d_list[0])

  # Flatten the 2D list and ensure every pixel is a tuple
  flat_pixels = []
  for row in rgba_2d_list:
    for p in row:
      if isinstance(p, int):
        # Unpack integer 0xRRGGBBAA to (R, G, B, A)
        flat_pixels.append(((p >> 24) & 0xFF, (p >> 16) & 0xFF, (p >> 8) & 0xFF, p & 0xFF))
      else:
        flat_pixels.append(p)

    # Create the image using Pillow's Image.new and putdata
  new_img = Image.new("RGBA", (width, height))
  new_img.putdata(flat_pixels)

  # Save to a byte buffer and return as BlobMedia
  img_byte_arr = io.BytesIO()
  new_img.save(img_byte_arr, format='PNG')
  return anvil.BlobMedia("image/png", img_byte_arr.getvalue(), name="converted_image.png")

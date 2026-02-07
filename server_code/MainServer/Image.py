import io
import anvil.server
import anvil.media
from PIL import Image

@anvil.server.callable
def image_to_rgba_list(media_obj):
  """Converts Media object to a 2D list of [R, G, B, A] lists."""
  with anvil.media.TempFile(media_obj) as f:
    with Image.open(f) as img:
      img = img.convert("RGBA")
      width, height = img.size
      # Get flat data as tuples, then convert each to a list
      pixels = [list(p) for p in img.getdata()]

    # Reshape into a 2D list: [height][width][rgba_list]
  return [pixels[i * width : (i + 1) * width] for i in range(height)]

@anvil.server.callable
def rgba_list_to_media(rgba_2d_list):
  """Converts a 2D list where each pixel is [R, G, B, A] back to Media."""
  if not rgba_2d_list:
    return None

  height = len(rgba_2d_list)
  width = len(rgba_2d_list[0])

  # Flatten the 2D list of lists into a 1D list of tuples
  # Pillow's putdata() requires tuples for the final image creation
  flat_tuples = []
  for row in rgba_2d_list:
    for p in row:
      # p is [R, G, B, A]
      flat_tuples.append(tuple(p))

    # Reconstruct the image
  new_img = Image.new("RGBA", (width, height))
  new_img.putdata(flat_tuples)

  # Save to bytes for Anvil Media
  img_byte_arr = io.BytesIO()
  new_img.save(img_byte_arr, format='PNG')

  return anvil.BlobMedia("image/png", img_byte_arr.getvalue(), name="reconstructed.png")

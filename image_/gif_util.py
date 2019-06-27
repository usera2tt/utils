from PIL import Image
from PIL import GifImagePlugin


def extract_first_frame(im: Image, filename: str):
    im.seek(0)
    im.save(filename)
   

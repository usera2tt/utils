from PIL import Image
from PIL import ImageFilter
import io
import base64
import time
import hashlib

from werkzeug.utils import secure_filename


class ImageManager:
    def __init__(self):
        pass

    @staticmethod
    def hash_filename(filename, raw_name_args):
        if not raw_name_args:
            raw_name_args = []
        filename = secure_filename(filename)
        extension = filename.split('.')[-1]
        filename = ''.join(map(lambda d: str(d), raw_name_args)) \
                   + hashlib.md5((str(time.time()) + filename).encode()).hexdigest() + '.' + extension
        return filename

    @staticmethod
    def load_image(image, b64=False):
        if b64:
            # image : b64 encoded
            im = Image.open(io.BytesIO(base64.b64decode(image)))
        else:
            # image : binary image
            im = Image.open(io.BytesIO(image))
        return im

    @staticmethod
    def to_square(im: Image):
        width, height = im.size
        new_width = min(width, height)
        im = im.crop((0, 0, new_width, new_width))
        return im

    @staticmethod
    def resize(im: Image, width):
        size = min(width, min(im.size))
        im = im.resize((size, size))
        return im

    @staticmethod
    def blur_image(im: Image, g_radius=8):
        return im.filter(ImageFilter.GaussianBlur(g_radius))

    @staticmethod
    def image_to_base64(im: Image):
        output = io.BytesIO()
        im = im.convert('RGB')
        im.save(output, format='jpeg')
        hex_data = output.getvalue()
        del im
        del output
        encoded = base64.b64encode(hex_data)
        return encoded

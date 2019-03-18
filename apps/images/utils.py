import sys
import uuid
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from typing import Tuple


class ImageCompress:
    """
    Implements logic to compress image with specific sizes and create one
    preview image for it.
    """

    COMPRESS_QUALITY = 80  # Output quality  of compression. Recommended range is (80,85)
    DEFAULT_ORIGINAL_SIZE = (780, 780)
    DEFAULT_THUMBNAIL_SIZE = (120, 120)

    def __init__(self, image, original_size: Tuple[int, int] = None, thumbnail_size: Tuple[int, int] = None):
        self.image = Image.open(image)
        self.original_size = original_size or self.DEFAULT_ORIGINAL_SIZE
        self.thumbnail_size = thumbnail_size or self.DEFAULT_THUMBNAIL_SIZE

    def get_new_size(self, size):
        if self.image.width > size[0] and self.image.height > size[1]:
            percentage = self.get_percentage(size)
            new_size = (self.image.width * percentage, self.image.height * percentage)
        else:
            new_size = self.image.width, self.image.height
        return map(int, new_size)

    def get_percentage(self, size):
        return size[0] / self.image.width if self.image.width <= self.image.height else size[1] / self.image.height

    def get_new_images(self):
        original_image = self.save_image(self.image, self.original_size)
        thumbnail_image = self.save_image(self.image, self.thumbnail_size)
        return original_image, thumbnail_image

    def save_image(self, image_temp, size):
        output_io_stream = BytesIO()
        image = image_temp.resize(self.get_new_size(size))
        image = image.convert('RGB')
        image.save(output_io_stream, format='JPEG', progressive=True,  optimize=True)
        output_io_stream.seek(0)
        return InMemoryUploadedFile(output_io_stream,
                                    'ImageField',
                                    uuid.uuid4().hex + '.jpg',
                                    'image/jpeg',
                                    sys.getsizeof(output_io_stream), None)

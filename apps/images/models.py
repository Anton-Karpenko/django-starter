from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.base.utils import custom_uuid
from .utils import ImageCompress


def image_path(instance, filename):
    return f'{instance._meta.model_name}/{instance.id}/{filename}'


class Image(TimeStampedModel):
    """
    An abstract base class model that provides 'image' and
    'preview_image' fields with compression. Keeps track of whether the
     original_image has changed to prevent unnecessary image compression.
    """

    id = models.CharField(
        max_length=11,
        primary_key=True,
        default=custom_uuid,
        editable=False,
    )
    original_image = models.ImageField(
        blank=True,
        null=True,
        upload_to=image_path
    )
    __original_image = None

    preview_image = models.ImageField(
        blank=True,
        null=True,
        upload_to=image_path,
        editable=False
    )

    class Meta:
        db_table = 'images'

    def save(self, **kwargs):
        if self.original_image and self.__original_image is not self.original_image:
            image_compressor = ImageCompress(self.original_image,
                                             original_size=kwargs.pop('original_size', None),
                                             thumbnail_size=kwargs.pop('thumbnail_size', None))
            self.original_image, self.preview_image = image_compressor.get_new_images()
        super().save(**kwargs)
        self.__original_image = self.original_image

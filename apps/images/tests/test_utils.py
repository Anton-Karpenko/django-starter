import pytest

from apps.images.models import Image

pytestmark = pytest.mark.django_db


class TestImageCompressor:

    @pytest.mark.parametrize('original_size, thumbnail_size',
                             [((780, 780), (120, 120)),
                              ((500, 500), (100, 100))])
    def test_final_sizes(self, temp_image, original_size, thumbnail_size):
        image = Image(original_image=temp_image)
        image.save(original_size=original_size, thumbnail_size=thumbnail_size)
        assert (image.preview_image.width, image.preview_image.height) == thumbnail_size
        assert (image.original_image.width, image.original_image.height) <= original_size

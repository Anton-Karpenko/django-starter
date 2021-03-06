from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from apps.base.utils import custom_uuid
from apps.images.models import Image
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    GENDER_CHOICES = (
        (MALE, _("Male")),
        (FEMALE, _("Female")),
        (OTHER, _("Other")),
    )

    id = models.CharField(
        max_length=11,
        primary_key=True,
        default=custom_uuid,
        editable=False,
    )
    username = models.CharField(
        max_length=24,
        unique=True,
        help_text=_('Max length is 24 symbols. Letters, digits and _/./_ only.'),
        validators=[
            validators.MinLengthValidator(1),
            validators.MaxLengthValidator(24),
        ],
        error_messages={'unique': _("A user with this nickname already exists.")},
        default=custom_uuid,
    )
    name = models.CharField(
        _("Full name of User"),
        max_length=60,
        validators=[validators.MaxLengthValidator(60),
                    validators.MinLengthValidator(1)],
    )
    email = models.EmailField(
        unique=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
    )
    birth_date = models.DateField(
        null=True,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active. '
                    'Unselect this instead of deleting accounts.'),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

    @property
    def is_new(self):
        # Only this data does not exist when a new user is filled with data from a social provider.
        return not any((self.name, self.gender, self.birth_date, self.profile_images_set.exists()))


class ProfileImage(TimeStampedModel):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='profile_images_set'
    )
    image = models.OneToOneField(
        'images.Image',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    @classmethod
    def create(cls, user, image):
        image = Image.objects.create(original_image=image)
        ProfileImage.objects.create(user=user, image=image)

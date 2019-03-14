from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

from .utils import create_data_filler


@receiver(pre_social_login)
def populate_profile(request, sociallogin, **kwargs):
    create_data_filler(sociallogin).populate()

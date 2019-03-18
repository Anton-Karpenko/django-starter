from datetime import datetime

from apps.base.utils import handle_upload_url_file
from apps.users.models import ProfileImage


class SocialDataFiller:
    values = 'image', 'birthday', 'gender'

    def __init__(self, sociallogin):
        self.sociallogin = sociallogin
        self.data = sociallogin.account.extra_data

    def set_image(self):
        raise NotImplementedError

    def set_birthday(self):
        raise NotImplementedError

    def set_gender(self):
        raise NotImplementedError

    def populate(self):
        for value in self.values:
            getattr(self, f'set_{value}')()


class FacebookDataFiller(SocialDataFiller):
    def set_birthday(self):
        birthday = self.data.get('birthday', '')
        if birthday:
            self.sociallogin.user.birth_date = datetime.strptime(birthday, '%m/%d/%Y').date()

    def set_image(self):
        image = handle_upload_url_file("http://graph.facebook.com/" + self.sociallogin.account.uid +
                                       "/picture?width=1000&height=1000")
        ProfileImage.create(user=self.sociallogin.user, image=image)

    def set_gender(self):
        self.sociallogin.user.gender = self.data.get('gender', '')


class GoogleDataFiller(SocialDataFiller):
    def set_birthday(self):
        pass

    def set_image(self):
        picture = self.data.get('picture')
        image = handle_upload_url_file(picture)
        ProfileImage.create(user=self.sociallogin.user, image=image)

    def set_gender(self):
        self.sociallogin.user.gender = self.data.get('gender', '')


def create_data_filler(sociallogin):
    if sociallogin.account.provider == 'facebook':
        return FacebookDataFiller(sociallogin)
    if sociallogin.account.provider == 'google':
        return GoogleDataFiller(sociallogin)

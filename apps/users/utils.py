from datetime import datetime


class SocialDataFiller:
    values = 'image', 'birthday', 'name', 'gender'

    def __init__(self, sociallogin):
        self.sociallogin = sociallogin
        self.data = sociallogin.account.extra_data

    def set_image(self):
        raise NotImplementedError

    def set_birthday(self):
        raise NotImplementedError

    def set_name(self):
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
        pass

    def set_name(self):
        self.sociallogin.user.name = self.data.get('name', '')

    def set_gender(self):
        self.sociallogin.user.gender = self.data.get('gender', '')


class GoogleDataFiller(SocialDataFiller):
    def set_birthday(self):
        pass

    def set_image(self):
        pass

    def set_name(self):
        self.sociallogin.user.name = self.data.get('name', '')

    def set_gender(self):
        self.sociallogin.user.gender = self.data.get('gender', '')


def create_data_filler(sociallogin):
    if sociallogin.account.provider == 'facebook':
        return FacebookDataFiller(sociallogin)
    if sociallogin.account.provider == 'google':
        return GoogleDataFiller(sociallogin)

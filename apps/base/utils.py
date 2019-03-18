import random
from urllib.request import build_opener

from django.core.files.temp import NamedTemporaryFile


def handle_upload_url_file(url):
    img_temp = NamedTemporaryFile()
    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1')]
    img_temp.write(opener.open(url).read())
    img_temp.flush()
    return img_temp


def custom_uuid():
    """
    Custom uuid consists of 11 symbols.
    :rtype: str
    :return: unique identifier
    """
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    return ''.join([random.choice(chars) for i in range(0, 11)])

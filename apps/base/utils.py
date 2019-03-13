import random


def custom_uuid():
    """
    Custom uuid consists of 11 symbols.
    :rtype: str
    :return: unique identifier
    """
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    return ''.join([random.choice(chars) for i in range(0, 11)])

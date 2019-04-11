# Created by Lionel Kornberger at 2019-04-08
from PIL import Image


class ExtendedImage(object):

    def __init__(self, path):
        self.__img = Image.open(path)
        self.__path = path

    def __getattr__(self, key):
        if key == '__img':
            #  http://nedbatchelder.com/blog/201010/surprising_getattr_recursion.html
            raise AttributeError()
        return getattr(self.__img, key)

    def scale(self, size):
        pass

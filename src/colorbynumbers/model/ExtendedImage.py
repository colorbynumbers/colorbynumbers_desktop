# Created by Lionel Kornberger at 2019-04-08


class ExtendedImage(object):

    def __init__(self, img):
        self.__img = img

    def __getattr__(self, key):
        if key == '__img':
            #  http://nedbatchelder.com/blog/201010/surprising_getattr_recursion.html
            raise AttributeError()
        return getattr(self.__img, key)

    def resize(self, size="DIN A4"):
        #Todo implement resizing to given DIN Format
        return ExtendedImage(self.__img.resize(size=size))

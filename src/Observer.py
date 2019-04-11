# Created by Lionel Kornberger at 2019-04-09


class Observer(object):
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        if observer in self.__observers:
            print(observer, 'already in subscribed observers')

        else:
            self.__observers.append(observer)

    def unregister_observer(self, observer):
        try:
            self.__observers.remove(observer)
        except ValueError:
            print('No such observer in subject')

    def notify_observers(self):
        # self.cur_time = time.time()
        for observer in self.__observers:
            observer.notify()

from abc import ABCMeta, abstractmethod

class DataProvider(object):
    __meta__ = ABCMeta

    @abstractmethod
    def get_key(self):
        return

    @abstractmethod
    def download_latest_data(self):
        return

    @abstractmethod
    def process_data(self, datafiles):
        return

from abc import ABCMeta, abstractmethod

# Interface defining interaction of data providers and generate script
class DataProvider(object):
    __meta__ = ABCMeta

    # Should return a unique string to identify the provider
    @abstractmethod
    def get_key(self):
        return

    # Should return a list of file-like objects containing datafiles needed by this provider
    @abstractmethod
    def download_latest_data(self):
        return

    # Will be passed a list of file-like objects with the same contents as download_latest_data returned, and should process them and return a dictionary with data to use in the template.
    @abstractmethod
    def process_data(self, datafiles):
        return

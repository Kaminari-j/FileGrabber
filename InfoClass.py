class FileInfo:
    FILE_NAME = None
    FILE_NAME_EN = None
    FILE_NAME_KO = None
    FILE_URL = None
    EXT = None
    PATH = None

    def __init__(self, file_url, title=None):
        if file_url:
            self.FILE_URL = file_url
            self.FILE_NAME = file_url.split('?')[0].split('/')[-1]
            self.FILE_NAME_EN = self.FILE_NAME.split('.')[0]
            self.FILE_NAME_KO = title if title else self.FILE_NAME_EN
            self.EXT = self.FILE_NAME.split('.')[1]
            # Todo: Pathのこと
            self.PATH = r'./FILES/' + self.FILE_NAME

    def print_file(self):
        print('FILE_URL: ' + self.FILE_URL)
        print('FILE_NAME_EN: ' + self.FILE_NAME_EN)
        print('FILE_NAME_KO: ' + self.FILE_NAME_KO)
        print('EXT: ' + self.EXT)
        print('PATH: ' + self.PATH)


# Todo: Change name to Webservices
class Websites(object):
    CLIEN = "clien"
    THEQOO = "theqoo"
    INSTAGRAM = "instagram"

    @staticmethod
    def get_websites_dict():
        import sys
        this_methods_name = sys._getframe().f_code.co_name
        return {website: domain
                for website, domain
                in Websites.__dict__.items()
                if website[:2] != '__'
                and website != this_methods_name}


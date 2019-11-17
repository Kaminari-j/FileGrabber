# Todo: Change name to Webservices
class Webservices(object):
    CLIEN = "clien"
    THEQOO = "theqoo"
    INSTAGRAM = "instagram"

    @staticmethod
    def get_webservices_dict():
        import sys
        this_methods_name = sys._getframe().f_code.co_name
        return {website: domain
                for website, domain
                in Webservices.__dict__.items()
                if website[:2] != '__'
                and website != this_methods_name}

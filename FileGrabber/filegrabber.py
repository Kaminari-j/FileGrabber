# -*- coding: utf-8 -*-
import urllib.request
import re
from FileGrabber.handler import grabbers
from FileGrabber.info import Webservices, File
from FileGrabber.handler import converter
import os


# Todo: Check valid website it is
# for examples,
# https://theqoo.net/index.php?mid=talk&filter_mode=normal&page=1 (No srl)
# https://m.clien.net/service/board/park?&od=T31&po=0 (No srl too)
def verify_website(url):
    url = url.lower()
    for key, domain in Webservices.get_webservices_dict().items():
        pattern = 'http(s)?://.*' + domain + '.*'
        if re.compile(pattern).match(url):
            return domain
    raise ValueError


def create_module(url: str):
    if url is None:
        raise ValueError

    website = verify_website(url)
    if website == Webservices.THEQOO:
        return grabbers.Theqoo()
    elif website == Webservices.CLIEN:
        return grabbers.Clien()
    elif website == Webservices.INSTAGRAM:
        return grabbers.Instagram()
    else:
        raise ValueError


def download_file(fi: File):
    return urllib.request.urlretrieve(fi.FILE_URL, "{0}".format(fi.PATH))


def do_grab(url: str, convert=False):
    module = create_module(url)
    for file in module.get_files(url):
        file.print_file()
        if not os.path.exists(file.PATH):
            download_file(file)
        if file.EXT == 'mp4' and convert is True:
            # Todo: Threading or make faster
            converter.convertFile(file.PATH, converter.TargetFormat.GIF)
            os.remove(file.PATH)


if __name__ == '__main__':
    testurl = r'https://www.clien.net/service/board/park/14155846?po=0&sk=title&sv=gif&groupCd=&pt=0'
    do_grab(testurl, False)

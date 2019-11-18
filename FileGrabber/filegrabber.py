# -*- coding: utf-8 -*-
import requests
import shutil
import re
from FileGrabber.handler import grabbers
from FileGrabber.info import Webservices, File
from FileGrabber.handler import converter
import os


# Todo: Check valid website it is
# for example,
# https://theqoo.net/index.php?mid=talk&filter_mode=normal&page=1
# https://m.clien.net/service/board/park?&od=T31&po=0
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
    # Todo: 403 Error (url: https://www.imageupload.net/upload-image/2019/11/17/GIF21.gif)
    r = requests.get(fi.FILE_URL, stream=True, headers={'User-agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        with open(fi.PATH, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        raise ValueError('Download Failed.')


def do_grab(url: str, convert=False):
    """
    URL의 gif 파일을 읽어들여 다운로드

    :param url: str
        파일을 다운로드할 페이지의 URL
    :param convert: bool
        mp4 -> gif 컨버트를 할지의 여부
    :return: None
    """
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

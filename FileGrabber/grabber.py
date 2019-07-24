# -*- coding: utf-8 -*-
from FileGrabber.InfoClass import Webservices, FileInfo
from FileGrabber import Module


# FileGrabber from FileGrabber proj
class FileGrabber:
    @staticmethod
    def grab_files(url):
        # Check Which website it is
        website = Module.Common.verify_website(url)
        # some url should be reformatted
        if website == Webservices.THEQOO:
            url = Module.Theqoo.reformat_url(url)
        elif website == Webservices.INSTAGRAM:
            url = Module.Instagram.reformat_url(url)
        
        # Get bs_obj
        bs_obj = Module.Common.getBsobj(url)

        if bs_obj:
            # verify website
            module = FileGrabber.create_module(website)

            # get article from document
            article = module.get_article(bs_obj)

            find_title = bs_obj.findAll('title')
            title = find_title[0].text if len(find_title) > 0 else ""
            files_on_url = module.collect_files_from_article(article)
            if files_on_url:
                files = list()
                for i, file_url in enumerate(files_on_url):
                    fi = FileInfo(file_url, title + '_' + str(i+1))
                    files.append(fi)
                return files

    @staticmethod
    def create_module(website: Webservices):
        if website == Webservices.THEQOO:
            return Module.Theqoo()
        elif website == Webservices.CLIEN:
            return Module.Clien()
        elif website == Webservices.INSTAGRAM:
            return Module.Instagram()
        else:
            raise ValueError

    @staticmethod
    def download_file(fi: FileInfo):
        Module.Common.download(fi)


if __name__ == '__main__':
    testurl = r'https://www.clien.net/service/board/park/13666299?od=T31&po=0&category=&groupCd='
    files = FileGrabber.grab_files(testurl)
    for f in files:
        f.print_file()
        print()

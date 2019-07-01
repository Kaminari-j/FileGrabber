# -*- coding: utf-8 -*-
from FileGrabber.InfoClass import Websites, FileInfo
from FileGrabber import Module


# FileGrabber from FileGrabber proj
class FileGrabber:
    @staticmethod
    def grab_files(url):
        # Check Which website it is
        website = Module.Common.verify_website(url)
        # some url should be reformatted
        if website == Websites.THEQOO:
            url = Module.Theqoo.reformat_url(url)
        elif website == Websites.INSTAGRAM:
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
                i = 1
                for file_url in files_on_url:
                    fi = FileInfo(file_url, title + '_' + str(i))
                    Module.Common.download(fi)
                    files.append(fi)
                    i += 1
                return files

    @staticmethod
    def create_module(website: Websites):
        if website == Websites.THEQOO:
            return Module.Theqoo()
        elif website == Websites.CLIEN:
            return Module.Clien()
        elif website == Websites.INSTAGRAM:
            return Module.Instagram()
        else:
            raise ValueError


if __name__ == '__main__':
    testurl = r'https://www.clien.net/service/board/park/13666299?od=T31&po=0&category=&groupCd='
    files = FileGrabber.grab_files(testurl)
    for f in files:
        f.print_file()
        print()

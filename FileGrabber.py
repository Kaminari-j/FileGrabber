# -*- coding: utf-8 -*-
from InfoClass import FileInfo, Websites
import FileGrabberModule


# FileGrabber from GrabPhotoFromCommunities proj
class FileGrabber:
    @staticmethod
    def grab_files(url):
        # Check Which website it is
        website = FileGrabberModule.Common.verify_website(url)
        # some url should be reformatted
        if website == Websites.THEQOO:
            url = FileGrabberModule.Theqoo.reformat_url(url)
        elif website == Websites.INSTAGRAM:
            url = FileGrabberModule.Instagram.reformat_url(url)
        
        # Get bs_obj
        bs_obj = FileGrabberModule.Common.getBsobj(url)

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
                    FileGrabberModule.Common.download(fi)
                    files.append(fi)
                    i += 1
                return files

    @staticmethod
    def create_module(website: Websites):
        if website == Websites.THEQOO:
            return FileGrabberModule.Theqoo()
        elif website == Websites.CLIEN:
            return FileGrabberModule.Clien()
        elif website == Websites.INSTAGRAM:
            return FileGrabberModule.Instagram()
        else:
            raise ValueError


if __name__ == '__main__':
    files = FileGrabber.grab_files('https://www.instagram.com/p/BvieWn7lLKR')
    for f in files:
        f.print_file()
        print()

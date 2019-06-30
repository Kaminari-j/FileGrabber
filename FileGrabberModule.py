# -*- coding: utf-8 -*-
import re
import urllib.request
from bs4 import BeautifulSoup, element
from InfoClass import FileInfo, Websites
import json


class Common:
    @staticmethod
    def getBsobj(url):
        try:
            html = urllib.request.urlopen(url)
            bs_obj = BeautifulSoup(html, features="html.parser")
            return bs_obj
        except:
            raise ValueError

    @staticmethod
    def download(fi: FileInfo):
        return urllib.request.urlretrieve(fi.FILE_URL, "{0}".format(fi.PATH))

    @staticmethod
    def verify_website(url):
        url = url.lower()
        for key, domain in Websites.get_websites_dict().items():
            pattern = 'http(s)?://.*' + domain + '.*'
            if re.compile(pattern).match(url):
                return domain
        raise ValueError

    # Todo: Check valid website it is
    # for examples,
    # https://theqoo.net/index.php?mid=talk&filter_mode=normal&page=1 (No srl)
    # https://m.clien.net/service/board/park?&od=T31&po=0 (No srl too)


class IFileGrabberModule:
    @classmethod
    def get_article(cls, bs_obj):
        raise NotImplementedError()

    @classmethod
    def collect_files_from_article(cls, article):
        raise NotImplementedError()


class Clien(IFileGrabberModule):
    def get_article(self, bs_obj):
        if isinstance(bs_obj, BeautifulSoup):
            return bs_obj.findAll("div", attrs={"class", "post_article"})[0]

    def collect_files_from_article(self, article):
        if article and isinstance(article, element.Tag):
            files = list()
            for item in article.findAll({'source', 'img', 'src'}):
                files.append(item.attrs['src'].split('?')[0])
            if len(files) > 0:
                return files


class Theqoo(IFileGrabberModule):
    def get_article(self, bs_obj):
        if isinstance(bs_obj, BeautifulSoup):
            return bs_obj.findAll({'article', 'itemprop'})[0]

    def collect_files_from_article(self, article):
        # when gfycat convert gfycat address here
        files = list()
        for line in article.text.split('\n'):
            pattern = 'http(s)?://gfycat\.com/\D+'
            re_res = re.compile(pattern).search(line)
            if re_res:
                files.append(self.convert_gfycat(re_res.string))
        if len(files) > 0:
            return [file for file in files if file is not None]

    # Todo : refactoring
    @staticmethod
    def reformat_url(url):
        reformatted_url = None
        pattern = '^http(s)?://theqoo\.net/[0-9]+$'
        if len(url.split('?')) == 1 and re.compile(pattern).search(url):
            reformatted_url = url
        else:
            for params in url.split('&'):
                pattern = 'document_srl'
                if re.compile(pattern).search(params):
                    reformatted_url = r'https://theqoo.net/' + params.split('=')[1]

        if reformatted_url:
            return reformatted_url
        else:
            raise ValueError

    @staticmethod
    def convert_gfycat(gfycat_url):
        gfyname = gfycat_url.split('/')[-1].split('.')[0]
        return 'https://thumbs.gfycat.com/' + gfyname + '-size_restricted.gif'


class Instagram(IFileGrabberModule):
    def get_article(self, bs_obj):
        if isinstance(bs_obj, BeautifulSoup):
            return json.loads(str(bs_obj))

    def collect_files_from_article(self, article):
        if article and isinstance(article, dict):
            files = list()
            base_data = article['graphql']['shortcode_media']
            media_type = base_data['__typename']

            if media_type == 'GraphVideo':
                files.append(base_data['video_url'])
            elif media_type == 'GraphImage':
                files.append(base_data['display_url'])
            elif media_type == 'GraphSidecar':
                for item in base_data['edge_sidecar_to_children']['edges']:
                    media_type = item['node']['__typename']
                    if media_type == 'GraphVideo':
                        files.append(item['node']['video_url'])
                    elif media_type == 'GraphImage':
                        files.append(item['node']['display_url'])

            return files

    @staticmethod
    def reformat_url(url):
        try:
            pattern = '^http(s)?://www\.instagram\.com/p/[\w|-]+/'
            return re.compile(pattern).match(url + '/')[0] + '?__a=1'
        except TypeError:
            raise TypeError('"' + url + '" Failed to reformat address')


if __name__ == '__main__':
    pass

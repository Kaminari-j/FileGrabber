# -*- coding: utf-8 -*-
import re
import json
import urllib.request
from bs4 import BeautifulSoup, element
from abc import *


class Grabbers(metaclass=ABCMeta):
    @abstractmethod
    def get_files(self, url):
        raise NotImplementedError()

    def grab_files(self, url):
        from FileGrabber.info import File
        url = self.reformat_url(url)

        # Get bs_obj
        # Todo: This process stuck with this url
        # https://cdn.clien.net/web/api/file/F01/9124365/435797c7760423.mp4
        bs_obj = self.get_bsobj(url)

        if bs_obj:
            # get article from document
            article = self.get_article(bs_obj)

            find_title = bs_obj.findAll('title')
            title = find_title[0].text if len(find_title) > 0 else ""
            files_on_url = self.collect_files_from_article(article)
            if files_on_url:
                files = list()
                for i, file_url in enumerate(files_on_url):
                    fi = File(file_url, title + '_' + str(i + 1))
                    files.append(fi)
                return files

    @staticmethod
    def get_bsobj(url):
        try:
            html = urllib.request.urlopen(url)
            bs_obj = BeautifulSoup(html, features="html.parser")
            return bs_obj
        except Exception as e:
            raise ValueError('Failed to get content : {0}'.format(e))

    @abstractmethod
    def get_article(self, bs_obj):
        raise NotImplementedError()

    @abstractmethod
    def collect_files_from_article(self, article):
        raise NotImplementedError()

    @abstractmethod
    def reformat_url(self, url):
        raise NotImplementedError()


class Clien(Grabbers):
    def get_files(self, url):
        return self.grab_files(url)

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

    def reformat_url(self, url):
        return url


class Theqoo(Grabbers):
    def get_files(self, url):
        return self.grab_files(url)

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

    def reformat_url(self, url):
        reformatted_url = None
        # Check if valid url
        if re.compile('http(s)?://theqoo\.net/.*[\d]{8,15}').search(url):
            # Find doc_srl (10digits number)
            search_doc_srl = re.compile('[\d]{8,15}').search(url)
            reformatted_url = r'https://theqoo.net/' + search_doc_srl.group()

        return reformatted_url if reformatted_url is not None else ValueError('URL is Invalid: ' + url)

    @staticmethod
    def convert_gfycat(gfycat_url):
        return 'https://thumbs.gfycat.com/' + \
                gfycat_url.split('/')[-1].split('.')[0] + \
                '-size_restricted.gif'


class Instagram(Grabbers):
    def get_files(self, url):
        return self.grab_files(url)

    def get_article(self, bs_obj):
        if isinstance(bs_obj, BeautifulSoup):
            return json.loads(str(bs_obj))

    def collect_files_from_article(self, article):
        if article and isinstance(article, dict):
            base_data = article['graphql']['shortcode_media']
            media_type = base_data['__typename']

            files = list()
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

    def reformat_url(self, url):
        try:
            pattern = '^http(s)?://www\.instagram\.com/p/[\w|-]+/'
            return re.compile(pattern).match(url + '/')[0] + '?__a=1'
        except TypeError:
            raise TypeError('"' + url + '" Failed to reformat address')


if __name__ == '__main__':
    pass

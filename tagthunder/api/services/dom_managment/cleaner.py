import copy

import bs4


class DOMCleaner:
    whitelist = ["alt", "href", "title", "role"]

    @classmethod
    def clean_dom(cls, soup: bs4.BeautifulSoup):
        soup = copy.copy(soup)

        for tag in soup.findAll(True):
            if not cls.remove_empty_tag(tag):
                cls.remove_attrs(tag)
        return soup

    @classmethod
    def remove_empty_tag(cls, tag):
        """
        Clean tag inplace
        :param tag:
        :return:
        """
        if len(tag.contents) == 0 and tag.name not in ["img"]:
            tag.decompose()
            return True
        return False

    @classmethod
    def remove_attrs(cls, tag):
        for attr in [attr for attr in tag.attrs if attr not in cls.whitelist]:
            del tag[attr]

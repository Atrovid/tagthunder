import bs4
import itertools


class TextContentExtractor:
    @classmethod
    def extract_alt(cls, soup):
        elements = soup.find_all(True, attrs={"alt": True})
        alts = [e["alt"] for e in elements]
        return alts

    @classmethod
    def extract_title(cls, soup):
        elements = soup.find_all(True, attrs={"title": True})
        titles = [e["title"] for e in elements]
        return titles

    @classmethod
    def tag_visible(cls, element):
        return (
                not element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']
                and not isinstance(element, bs4.Comment)
        )

    @classmethod
    def extract_text(cls, soup):
        texts = soup.find_all(text=True)
        visible_texts = filter(cls.tag_visible, texts)
        visible_texts = list(t.strip() for t in visible_texts)
        visible_texts = list(filter(None, visible_texts))

        return visible_texts

    @classmethod
    def extract_all_text(cls, soup):
        lists = [
            cls.extract_text(soup),
            cls.extract_title(soup),
            cls.extract_alt(soup)
        ]
        return list(itertools.chain.from_iterable(lists))

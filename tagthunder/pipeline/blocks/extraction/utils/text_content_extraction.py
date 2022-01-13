import copy
import itertools

import inscriptis

from pipeline.models.responses import HTMLPP


class TextExtractor:

    @classmethod
    def extract_alt(cls, htmlpp: HTMLPP):
        elements = htmlpp.find_all(True, attrs={"alt": True})
        alts = [e["alt"] for e in elements]
        return alts

    @classmethod
    def extract_title(cls, htmlpp: HTMLPP):
        elements = htmlpp.find_all(True, attrs={"title": True})
        titles = [e["title"] for e in elements]
        return titles

    @classmethod
    def extract_text(cls, htmlpp: HTMLPP):
        return [s.strip() for s in inscriptis.get_text(str(htmlpp)).replace('\n\n', '\n').split("\n") if len(s)]

    @classmethod
    def caption_images(cls, htmlpp: HTMLPP):
        raise NotImplementedError

    @classmethod
    def extract(cls, htmlpp: HTMLPP):
        htmlpp = copy.copy(htmlpp)
        htmlpp.remove_unusable_tags()
        lists = [
            cls.extract_title(htmlpp),
            cls.extract_alt(htmlpp),
            cls.extract_text(htmlpp),
        ]
        return list(itertools.chain.from_iterable(lists))

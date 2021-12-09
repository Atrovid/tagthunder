import itertools


class TextExtractor:
    @classmethod
    def extract_alt(cls, htmlpp):
        elements = htmlpp.find_all(True, attrs={"alt": True})
        alts = [e["alt"] for e in elements]
        return alts

    @classmethod
    def extract_title(cls, htmlpp):
        elements = htmlpp.find_all(True, attrs={"title": True})
        titles = [e["title"] for e in elements]
        return titles

    @classmethod
    def extract_text(cls, htmlpp):
        texts = htmlpp.find_all(lambda tag: tag.is_usable, text=True)
        return list(t.strip() for t in texts)

    @classmethod
    def caption_images(cls, htmlpp):
        raise NotImplementedError

    @classmethod
    def extract(cls, htmlpp):
        lists = [
            cls.extract_text(htmlpp),
            cls.extract_title(htmlpp),
            cls.extract_alt(htmlpp)
        ]
        return list(itertools.chain.from_iterable(lists))

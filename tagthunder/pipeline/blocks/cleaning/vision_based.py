import bs4

from pipeline.blocks.cleaning._abstract import AbstractCleaningBlock
from pipeline.models.responses import HTMLPP, HTMLP
from pipeline.models.web_elements import HTMLPTag, HTMLPPTag


class VisionBased(AbstractCleaningBlock):
    USELESS_TAGS = ["title", "link", "script", "noscript", "style", "doctype", "head", "base", "command",
                    "meta", "br"]

    def __call__(self, htmlp: HTMLP) -> HTMLPP:
        res = HTMLPP(htmlp.markup)
        self.remove_comments(res)
        self.remove_useless_tags(res)

        return res

    @classmethod
    def remove_comments(cls, htmlpp: HTMLPP):
        for comment in htmlpp.find_all(text=lambda text: isinstance(text, bs4.Comment)):
            comment.extract()
        return htmlpp

    @classmethod
    def remove_useless_tags(cls, htmlpp: HTMLPP):
        for tag in htmlpp.find_all(lambda tag: tag.name in cls.USELESS_TAGS):
            tag.extract()
        return htmlpp

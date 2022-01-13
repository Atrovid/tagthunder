from abc import ABC, abstractmethod

import bs4

from pipeline.models.responses import HTMLPP, HTMLP
from pipeline.models.web_elements import HTMLPTag, HTMLPPTag

from pipeline.blocks._abstract import AbstractPipelineBlock


class AbstractCleaningBlock(AbstractPipelineBlock):
    NON_CONTAINER_TAGS = ["img"]

    @abstractmethod
    def __call__(self, *, htmlp: HTMLP) -> HTMLPP:
        ...

    @classmethod
    @abstractmethod
    def _is_usable_tag(cls, tag: HTMLPTag) -> bool:
        ...

    @classmethod
    def mark_as_usable_tag(cls, tag: HTMLPTag):
        tag.attrs[HTMLPPTag.IS_USABLE_HTML_ATTR_KEY] = str(cls._is_usable_tag(tag)).lower()

    @classmethod
    def contains_comment(cls, htmlp: HTMLP):
        return htmlp.contains_comments(recursive=True)

    @classmethod
    def remove_comments(cls, htmlp: HTMLP):
        for comment in htmlp.get_comments(True):
            comment.extract()

    @classmethod
    def is_empty_tag(cls, tag: HTMLPTag) -> bool:
        return all((
            tag.name not in cls.NON_CONTAINER_TAGS,
            not list(tag.text.strip()),
            all([cls.is_empty_tag(t) and t.name not in cls.NON_CONTAINER_TAGS for t in tag()])
        ))

    @classmethod
    def is_flat_tag(cls, tag: HTMLPTag) -> bool:
        return not tag.bbox.is_visible

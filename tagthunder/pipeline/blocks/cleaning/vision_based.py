from typing import List, Callable, Iterable

import bs4

from pipeline.blocks.cleaning._abstract import AbstractCleaningBlock
from pipeline.models.responses import HTMLPP, HTMLP
from pipeline.models.web_elements import HTMLPTag


class VisionBased(AbstractCleaningBlock):
    USELESS_TAGS = ["title", "link", "script", "noscript", "style", "doctype", "head", "base", "command",
                    "meta", "br"]
    NON_CONTAINER_TAGS = ["img"]

    def __call__(self, htmlp: HTMLP) -> HTMLPP:
        for tag in htmlp.find_all(True):
            if any([c(tag) for c in self.remove_conditions]):
                tag.decompose()
            else:
                self.mark_as_usable_tag(tag, self._is_usable_tag(tag))

        return HTMLPP(htmlp)

    @classmethod
    def _is_usable_tag(cls, tag: HTMLPTag):
        return (tag.bbox.is_usable
                and not any([
                    tag.styles.get("display") == "none",
                    tag.styles.get("visiblity") == "hidden",
                    tag.styles.get("hidden") == "true",
                ])
                )

    @property
    def remove_conditions(self) -> Iterable[Callable]:
        return (
            self.is_comments,
            self.is_useless_tag,
            self.is_empty_tag,
            self.is_flat_tag
        )

    @classmethod
    def is_comments(cls, tag: HTMLPTag) -> bool:
        return isinstance(tag.text, bs4.Comment)

    @classmethod
    def is_useless_tag(cls, tag: HTMLPTag) -> bool:
        return tag.name in cls.USELESS_TAGS

    @classmethod
    def is_empty_tag(cls, tag: HTMLPTag) -> bool:
        return (
                tag.name not in cls.NON_CONTAINER_TAGS
                and not list(tag.strings)
                and not tag.find_all(lambda sub_tag: sub_tag.name in cls.NON_CONTAINER_TAGS)
        )

    @classmethod
    def is_flat_tag(cls, tag: HTMLPTag) -> bool:
        return tag.bbox.is_usable

from typing import Callable, Iterable

from pipeline.blocks.cleaning._abstract import AbstractCleaningBlock
from pipeline.models.responses import HTMLPP, HTMLP
from pipeline.models.web_elements import HTMLPTag


class VisionBased(AbstractCleaningBlock):
    USELESS_TAGS = ["title", "link", "script", "noscript", "style", "doctype", "head", "base", "command",
                    "meta", "br"]

    def __call__(self, htmlp: HTMLP) -> HTMLPP:
        self.remove_comments(htmlp)
        for tag in list(htmlp())[::-1]:
            if any([c(tag) for c in self.remove_conditions]):
                tag.extract()
            else:
                self.mark_as_usable_tag(tag)

        return HTMLPP(str(htmlp))

    @classmethod
    def _is_usable_tag(cls, tag: HTMLPTag):
        return all([
            tag.styles.get("display") != "none",
            tag.styles.get("visibility") != "hidden",
        ])

    @property
    def remove_conditions(self) -> Iterable[Callable]:
        return (
            self.is_useless_tag,
            self.is_empty_tag,
            self.is_flat_tag
        )

    @classmethod
    def is_useless_tag(cls, tag: HTMLPTag) -> bool:
        return tag.name in cls.USELESS_TAGS

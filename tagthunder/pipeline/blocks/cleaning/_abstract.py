from abc import ABC, abstractmethod

from pipeline.models.responses import HTMLPP, HTMLP
from pipeline.models.web_elements import HTMLPTag, HTMLPPTag


class AbstractCleaningBlock(ABC):

    @abstractmethod
    def __call__(self, *, htmlp: HTMLP) -> HTMLPP:
        ...

    @classmethod
    @abstractmethod
    def _is_usable_tag(cls, tag: HTMLPTag):
        ...

    @classmethod
    def mark_as_usable_tag(cls, tag: HTMLPTag, value: bool):
        tag.attrs[HTMLPPTag.IS_USABLE_HTML_ATTR_KEY] = str(value)

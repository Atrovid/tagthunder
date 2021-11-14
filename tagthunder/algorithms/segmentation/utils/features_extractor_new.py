import json
from abc import ABC, abstractmethod

import bs4
import re

from algorithms.models.responses import HTMLPP


class AbstractFeaturesExtractor(ABC):

    def __call__(self, htmlpp: HTMLPP):
        root = bs4.BeautifulSoup(htmlpp.__root__, "html.parser")
        results = []
        self.walker(root, results)

        return results

    @classmethod
    def walker(cls, node, results):
        if node.name is not None:
            for child in cls.children(node):
                if cls.to_be_kept(child):
                    results.append(child)
                else:
                    cls.walker(child, results)

    @classmethod
    @abstractmethod
    def to_be_kept(cls, node) -> bool:
        ...

    @classmethod
    def children(cls, node):
        return node.find_all(True, recursive=False)


class LastBlocks(AbstractFeaturesExtractor):

    @classmethod
    def to_be_kept(cls, node) -> bool:
        tests = [
            cls.is_visible,
            cls.is_last_block
        ]
        return all(test(node) for test in tests)


    @classmethod
    def is_visible(cls, node) -> bool:
        try:
            return node.attrs["data-cleaned"] == "false"
        except KeyError:
            return False

    @classmethod
    def is_last_block(cls, node) -> bool:
        try:
            children = []
            if re.findall("display:block", node.attrs["data-style"]):
                cls.walker(node, children)

            return not children
        except KeyError:
            return False

if __name__ == '__main__':
    json_file = "../../data/html++/calvados.raw.json"
    with open(json_file, "r") as f:
        content = json.load(f)
        htmlpp = HTMLPP.parse_obj(content["html"])

    extractor = LastBlocks()

    elements = extractor(htmlpp)
    print(len(elements))

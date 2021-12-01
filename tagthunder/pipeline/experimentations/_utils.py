import json

from pipeline.models.responses import HTMLPP


def get_htmlpp(json_file) -> HTMLPP:
    with open(json_file, "r") as f:
        content = json.load(f)
        htmlpp = HTMLPP(content["html"])

    return htmlpp

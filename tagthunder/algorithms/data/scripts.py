import json

import bs4

from algorithms.models.responses import HTMLPP


def open_json(file):
    with open(file, "r") as f:
        content = json.load(f)
    return HTMLPP.parse_obj(content["html"])


def keep_styles(htmlpp, styles):
    root = bs4.BeautifulSoup(htmlpp.__root__)
    nodes = root.find_all(True, attrs={
        "data-style": True
    })

    for node in nodes:
        clean_styles(node, styles)

    return root

def styles_to_str(styles):
    return ';'.join(':'.join(sv) for sv in styles)


def clean_styles(node, to_be_kept):
    styles = node.attrs["data-style"]
    styles = [sv.split(":") for sv in styles.split(";") if ":" in sv]
    styles = filter(lambda s: s[0] in to_be_kept, styles)
    node.attrs["data-style"] = styles_to_str(styles)

    return node


def export_to_json(html, json_file):
    with open(json_file, "w") as f:
        json.dump(html.prettify(), f)

def main(file, styles):
    return keep_styles(open_json(file), styles)


if __name__ == '__main__':
    json_file = "html++/calvados.raw.json"

    styles = [
        "display"
    ]

    res = main(json_file, styles).prettify()
    print(res)



import json
import os.path

import bs4

from pipeline.models.responses import HTMLPP


def open_json(file):
    with open(file, "r") as f:
        content = json.load(f)
    return bs4.BeautifulSoup(content["html"])


def keep_styles(root, styles):
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


def remove_scripts(node):
    for tag in node.select("script"):
        tag.extract()

    return node


def dump(html, file, ext):
    with open(file, "w") as f:
        if ext == 'json':
            json.dump(html, f)
        else:
            f.write(html)


def main(file, styles, out_file):
    html = keep_styles(remove_scripts(open_json(file)), styles)
    print(html)
    data = {"html": html.prettify()}
    dump(str(html), out_file, out_file.split(".")[-1])


if __name__ == '__main__':
    dir = "html++"
    file = "calvados.raw"
    ext = "json"
    json_file = os.path.join(dir, f"{file}.{ext}")

    styles = [
        "display"
    ]

    main(json_file, styles, os.path.join(dir, f"calvados.html"))

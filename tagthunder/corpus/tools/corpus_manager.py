from typing import Dict, Any

import os, subprocess

from pydantic import HttpUrl


class Wget:
    """
    Contains operation to download web page or entire website.
    """
    DATA_DIR = os.path.abspath("../data")
    COMMAND = "wget"
    BASE_ARGS = [
        "--page-requisites",
        "--convert-links",
        "-P", DATA_DIR,
    ]

    @classmethod
    def save_page(cls, url: HttpUrl):
        command = [
            cls.COMMAND,
            *cls.BASE_ARGS,
            str(url)
        ]

        cls.subprocess(command)

    @classmethod
    def save_site(cls, url: HttpUrl, depth: int = 5):
        command = [
            cls.COMMAND,
            *cls.BASE_ARGS,
            "--recursive",
            "--level", depth,
            "--no-parent",
            str(url)
        ]

        cls.subprocess(command)

    @classmethod
    def subprocess(self, command):
        wget = subprocess.Popen(command, stdin=None, stdout=None, stderr=None, close_fds=False)
        wget.wait()


if __name__ == '__main__':
    corpus_manager = Wget()
    corpus_manager.save_page("https://www.calvados.fr/accueil/le-departement.html")

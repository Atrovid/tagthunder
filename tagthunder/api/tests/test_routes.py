import io
import zipfile

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.routers.routes import Routes, queries, router

HEADERS = {"X-Token": "coneofsilence"}

client = TestClient(app)


def test_augmentation():
    body = {
        "url": "https://www.example.com",
        "algorithm": {
            "name": "puppeteer",
            "parameters": {
                "page_width": 1200,
                "page_height": 1200,
                "styles": [
                    "display",
                    "visibility"
                ]
            }
        }
    }

    response = client.post(
        url=f'{router.prefix}{Routes.AUGMENTATION}',
        headers=HEADERS,
        json=body
    )

    assert response.status_code == 200


def test_pipeline():
    body = {
        # "url": "https://www.example.com",
        "url": "https://www.calvados.fr",
        "htmlpp": "",
        "recompute": False,
        "augmentation": {
            "name": "puppeteer",
            "parameters": {
                "page_width": 1200,
                "page_height": 1200,
                "styles": [
                    "display",
                    "visibility"
                ]
            }
        },
        "cleaning": {
            "name": "vision_based",
            "parameters": {}
        },
        "segmentation": {
            "name": "TDBU",
            "parameters": {
                "nb_zones": 5
            }
        },
        "extraction": {
            "name": "yake",
            "parameters": {
                "nb_keywords": 5,
                "max_ngram_size": 4,
                "window_size": 3,
                "language": "fr"
            }
        },
        "vocalization": {
            "name": "playback_speed_area_size",
            "parameters": {
                "lang_detector": "google_translate",
                "tts_engine": "google_tts"
            }
        }
    }

    response = client.post(
        url=f'{router.prefix}{Routes.PIPELINE}',
        headers=HEADERS,
        json=body
    )

    assert response.status_code == 200

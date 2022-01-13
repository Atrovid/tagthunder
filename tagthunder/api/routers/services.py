import csv
import enum
import io
import zipfile
from typing import Optional

import fastapi
import toolz

from pydantic import HttpUrl

import api.models.schemas as schemas
import api.models.factories as factories
import api.configurations.pipeline as algorithms_conf


class AlgorithmServices:

    @classmethod
    def augmentation(cls, url: [HttpUrl], algorithm_name: str, parameters) -> Optional[schemas.HTMLP]:
        algorithm = cls.get_algorithm("augmentation", algorithm_name, **parameters)
        htmlp = algorithm(url)
        return factories.Responses.HTMLP(htmlp)

    @classmethod
    def cleaning(cls, htmlp: schemas.HTMLP, algorithm_name: str, parameters) -> schemas.HTMLPP:
        algorithm = cls.get_algorithm("cleaning", algorithm_name, **parameters)
        html_cleaned = algorithm(factories.AlgorithmInput.HTMLP(htmlp))
        return factories.Responses.HTMLPP(html_cleaned)

    @classmethod
    def segmentation(cls, htmlpp: schemas.HTMLPP, algorithm_name: str, parameters) -> schemas.Segmentation:
        algorithm = cls.get_algorithm("segmentation", algorithm_name, **parameters)
        segmentation = algorithm(factories.AlgorithmInput.HTMLPP(htmlpp))
        return factories.Responses.Segmentation(segmentation)

    @classmethod
    def extraction(cls, segmentation: schemas.Segmentation, algorithm_name: str, parameters) -> schemas.Segmentation:
        algorithm = cls.get_algorithm("extraction", algorithm_name, **parameters)
        segmentation = algorithm(factories.AlgorithmInput.Segmentation(segmentation))
        return factories.Responses.Segmentation(segmentation)

    @classmethod
    def vocalization(cls, segmentation: schemas.Segmentation, algorithm_name: str,
                     parameters) -> fastapi.responses.StreamingResponse:
        algorithm = cls.get_algorithm("vocalization", algorithm_name, **parameters)
        vocalization = algorithm(factories.AlgorithmInput.Segmentation(segmentation))
        # for f in vocalization:
        #     play_song(f)
        zip = MiscServices.zip_files(
            files=vocalization,
            file_name_func=lambda file: f"zone_{file.zone_id}.wav"
        )
        response = fastapi.responses.StreamingResponse(iter([zip.getvalue()]),
                                                       media_type="application/x-zip-compressed")
        response.headers["Content-Disposition"] = "attachment; filename=vocalization.zip"

        return response

    @classmethod
    def get_algorithm(cls, block_type, name, **parameters):
        algo = algorithms_conf.pipeline_blocks[block_type].get_algorithm(name)
        parameters = cls.prepare_parameters(parameters)
        algo.config(**parameters)
        return algo

    @classmethod
    def prepare_parameters(cls, parameters):
        def manage_enum(value):
            if isinstance(value, enum.Enum):
                return value.value
            return value

        return toolz.valmap(manage_enum, parameters)


class MiscServices:
    @classmethod
    def zip_files(cls, files, file_name_func):
        zipped_file = io.BytesIO()
        with zipfile.ZipFile(zipped_file, "a", zipfile.ZIP_DEFLATED) as zipped:
            for i, f in enumerate(files):
                f.seek(0)
                zipped.writestr(file_name_func(f), f.read())
        zipped_file.seek(0)
        return zipped_file

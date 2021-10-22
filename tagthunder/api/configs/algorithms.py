import enum
from typing import Type

import devtools as devtools

import tagthunder.algorithms as algorithms
import pydantic


class ParametersModelFactory:

    @classmethod
    def meta(cls, algorithm_name: str, **kwargs) -> Type[pydantic.BaseModel]:
        """

        :param algorithm_name: must be in CamelCase
        :param kwargs:
        :return:
        """
        return pydantic.create_model(f'{algorithm_name}Parameters', **kwargs)

    @classmethod
    def extraction(cls, algorithm_name: str, nb_keywords: int, **kwargs) -> Type[pydantic.BaseModel]:
        return cls.meta(
            algorithm_name,
            nb_keywords=(int, pydantic.Field(nb_keywords, description="Number of keywords / keyphrases.")),
            **kwargs
        )


class AlgorithmConfig(pydantic.BaseModel):
    name: str
    enable: bool
    algorithm: object
    parameters: Type[pydantic.BaseModel]

    class Config:
        arbitrary_types_allowed = True


@enum.unique
class ExtractionAlgorithms(enum.Enum):

    mots_blancs = AlgorithmConfig(
        name="mots_blancs",
        enable=False,
        algorithm=algorithms.extraction.MotsBlancs(),
        parameters=ParametersModelFactory.extraction(
            "MotsBlancs",
            nb_keywords=5
        )
    )

    yake = AlgorithmConfig(
        name="yake",
        enable=True,
        algorithm=algorithms.extraction.Yake(),
        parameters=ParametersModelFactory.extraction(
            "Yake",
            nb_keywords=5,
            max_ngram_size=(int, pydantic.Field(4, description="Maximal length of the keyprhases.")),
            window_size=(int, pydantic.Field(3, description="Window size")),
            language=(str, pydantic.Field("fr", description="Text content language"))
        )
    )

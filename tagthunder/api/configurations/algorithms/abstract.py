import abc
import enum
from typing import Type, Iterable

import algorithms as algorithms
import pydantic


class ParametersModelFactory:

    @classmethod
    def meta(cls, algorithm_name: str, **kwargs) -> Type[pydantic.BaseModel]:
        """

        :param algorithm_name: must be in snake_case
        :param kwargs:
        :return:
        """

        def name_validator(cls, v):
            assert v == algorithm_name
            return v

        query_model_name = ''.join(word.title() for word in algorithm_name.split('_')) + 'Query'
        parameters = pydantic.create_model(f"{query_model_name}Parameters", **kwargs)

        validators = {
            "name_validator": pydantic.validator("name", allow_reuse=True)(name_validator),
            "parameters_validator": pydantic.validator("*", allow_reuse=True)
        }

        return pydantic.create_model(
            query_model_name,
            name=algorithm_name,
            parameters=parameters(),
            __validators__=validators,
        )

    @classmethod
    def extraction(cls, algorithm_name: str, nb_keywords: int, **kwargs) -> Type[pydantic.BaseModel]:
        return cls.meta(
            algorithm_name,
            nb_keywords=(int, pydantic.Field(nb_keywords, description="Number of keywords / keyphrases.")),
            **kwargs
        )

    @classmethod
    def segmentation(cls, algorithm_name: str, nb_zones: int, le: int = None, ge: int = None, **kwargs) -> Type[
        pydantic.BaseModel]:
        return cls.meta(
            algorithm_name,
            nb_zones=(int, pydantic.Field(nb_zones, description="Number of zones", le=le, ge=ge)),
            **kwargs
        )

    @classmethod
    def cleaning(cls, algorithm_name: str, **kwargs) -> Type[pydantic.BaseModel]:
        return cls.meta(
            algorithm_name,
            **kwargs
        )


class AlgorithmConfig(pydantic.BaseModel):
    name: str
    enable: bool
    algorithm: object
    query: Type[pydantic.BaseModel]

    class Config:
        arbitrary_types_allowed = True


class ABCEnumMeta(abc.ABCMeta, enum.EnumMeta):
    pass


@enum.unique
class AlgorithmsEnum(enum.Enum, metaclass=ABCEnumMeta):
    @classmethod
    @property
    @abc.abstractmethod
    def default_query(cls):
        raise NotImplementedError()

    @classmethod
    @property
    def queries(cls):
        return [query() for query in cls.query_types]

    @classmethod
    @property
    def query_types(cls):
        return tuple([algo.value.query for _, algo in cls.__members__.items() if algo.value.enable])

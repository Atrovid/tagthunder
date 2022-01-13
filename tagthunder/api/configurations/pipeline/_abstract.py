import abc
import enum
from typing import Type, Iterable, Optional, Union

import pydantic


class BlockConfig(pydantic.BaseModel):
    name: str
    enable: bool
    algorithm: object
    query: Type[pydantic.BaseModel]

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def build_request_body(cls, algorithm_name: str, **kwargs) -> Type[pydantic.BaseModel]:
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


class ABCEnumMeta(abc.ABCMeta, enum.EnumMeta):
    pass


@enum.unique
class BlocksEnum(enum.Enum, metaclass=ABCEnumMeta):
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
    def query_types(cls) -> tuple:
        return tuple([algo.value.query for _, algo in cls.__members__.items() if algo.value.enable])

    @classmethod
    def get_algorithm(cls, name):
        entry = cls[name].value
        if entry.enable:
            return entry.algorithm
        else:
            raise KeyError(f"{name} algorithm is not available.")

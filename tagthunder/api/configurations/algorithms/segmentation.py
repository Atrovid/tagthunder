import pydantic as pydantic

from api.configurations.algorithms.abstract import AlgorithmsEnum, AlgorithmConfig, ParametersModelFactory
import algorithms as algorithms


class SegmentationAlgorithms(AlgorithmsEnum):
    tdbu = AlgorithmConfig(
        name="TDBU",
        enable=True,
        algorithm=algorithms.segmentation.TopDownBottomUp(),
        query=ParametersModelFactory.segmentation(
            "TDBU",
            nb_zones=5
        )
    )

    ge = AlgorithmConfig(
        name="GE",
        enable=False,
        algorithm=algorithms.segmentation.GuidedExpansion(),
        query=ParametersModelFactory.segmentation(
            "GE",
            nb_zones=5
        )
    )

    @classmethod
    @property
    def default_query(cls):
        return cls.tdbu.value.query()

import algorithms
import pydantic

class ParametersModelFactory:

    @classmethod
    def meta(cls, algorithm_name: str, **kwargs):
        """

        :param algorithm_name: must be in CamelCase
        :param kwargs:
        :return:
        """
        return pydantic.create_model(f'{algorithm_name}Parameters', **kwargs)

    @classmethod
    def extraction(cls, algorithm_name:str, nb_keywords:int, **kwargs):
        return cls.meta(
            algorithm_name,
            nb_keywords=(int, pydantic.Field(nb_keywords, description="Number of keywords / keyphrases."))
        )

EXTRACTION_ALGORITHMS = {
    "yake": {
        "enable": True,
        "algorithm": algorithms.extraction.Yake,
        "parameters": ParametersModelFactory.extraction(
            "Yake",
            nb_keywords=5,
            max_ngram_size=(int, pydantic.Field(4, description="Maximal length of the keyprhases.")),
            window_size=(int, pydantic.Field(3, description="Window size")),
            language=(str, pydantic.Field("fr", description="Text content language"))
        )
    },

    "mots_blancs" : {
        "enable": True,
        "algorithm": algorithms.extraction.MotsBlancs,
        "parameters": ParametersModelFactory.extraction(
            "MotsBlancs",
            nb_keywords=5
        )
    }
}

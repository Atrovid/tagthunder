from api.configurations.pipeline._abstract import BlocksEnum, AlgorithmConfig, ParametersModelFactory
import pipeline.blocks.vocalization


class VocalizationBlocks(BlocksEnum):
    google_tts = AlgorithmConfig(
        name="google_tts",
        enable=True,
        algorithm=pipeline.blocks.vocalization.GoogleTTS(),
        query=ParametersModelFactory.cleaning(
            "google_tts"
        )
    )

    @classmethod
    @property
    def default_query(cls):
        return cls.google_tts.value.query()

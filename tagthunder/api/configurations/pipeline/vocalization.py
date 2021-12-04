from api.configurations.pipeline._abstract import BlocksEnum, BlockConfig, ParametersModelFactory
import pipeline.blocks.vocalization


class VocalizationBlocks(BlocksEnum):
    google_tts = BlockConfig(
        name="google_tts",
        enable=True,
        algorithm=pipeline.blocks.vocalization.GoogleTTS(),
        query=ParametersModelFactory.vocalization(
            "google_tts"
        )
    )

    @classmethod
    @property
    def default_query(cls):
        return cls.google_tts.value.query()

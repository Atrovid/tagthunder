import pipeline.models.responses as algos_responses
import api.models.schemas as schemas


class AlgorithmInput:
    @classmethod
    def HTMLP(cls, htmlp: schemas.HTMLP) -> algos_responses.HTMLP:
        return algos_responses.HTMLP(htmlp.__root__)

    @classmethod
    def HTMLPP(cls, htmlpp: schemas.HTMLPP) -> algos_responses.HTMLPP:
        return algos_responses.HTMLPP(htmlpp.__root__)

    @classmethod
    def Keyword(cls, keyword: schemas.Keyword) -> algos_responses.Keyword:
        return algos_responses.Keyword(text=keyword.text, score=keyword.score)

    @classmethod
    def Keywords(cls, keywords: schemas.Keywords) -> algos_responses.Keywords:
        return [cls.Keyword(k) for k in keywords]

    @classmethod
    def Zone(cls, zone: schemas.Zone) -> algos_responses.Zone:
        return algos_responses.Zone(
            id=zone.id,
            htmlpp=cls.HTMLPP(zone.htmlpp),
            keywords=[cls.Keyword(kw) for kw in zone.keywords]
        )

    @classmethod
    def Segmentation(cls, segmentation: schemas.Segmentation) -> algos_responses.Segmentation:
        return algos_responses.Segmentation(
            zones=[cls.Zone(zone) for zone in segmentation.__root__]
        )


class Responses:

    @classmethod
    def HTML(cls, html: str) -> schemas.HTML:
        return schemas.HTML(__root__=html)

    @classmethod
    def HTMLP(cls, htmlp: algos_responses.HTMLP) -> schemas.HTMLP:
        return schemas.HTMLP(__root__=str(htmlp))

    @classmethod
    def HTMLPP(cls, htmlpp: algos_responses.HTMLPP) -> schemas.HTMLPP:
        return schemas.HTMLPP(__root__=str(htmlpp))

    @classmethod
    def Keyword(cls, keyword: algos_responses.Keyword) -> schemas.Keyword:
        return schemas.Keyword(text=keyword.text, score=keyword.score)

    @classmethod
    def Keywords(cls, keywords: algos_responses.Keywords) -> schemas.Keywords:
        return [cls.Keyword(k) for k in keywords]

    @classmethod
    def Zone(cls, zone: algos_responses.Zone) -> schemas.Zone:
        return schemas.Zone(
            id=zone.id,
            htmlpp=cls.HTMLPP(zone.htmlpp),
            keywords=cls.Keywords(zone.keywords)
        )

    @classmethod
    def Segmentation(cls, segmentation: algos_responses.Segmentation) -> schemas.Segmentation:
        return schemas.Segmentation(
            __root__=[cls.Zone(zone) for zone in segmentation.zones]
        )

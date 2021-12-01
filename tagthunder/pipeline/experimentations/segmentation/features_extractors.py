import json

import pipeline.experimentations.segmentation.visualisation as visualisation
import pipeline.blocks.segmentation.clustering.utils.features_extractors as features_extractors
from pipeline.models.responses import HTMLPP
import pipeline.experimentations._utils as expe_utils


def extraction(htmlpp: HTMLPP, extractor: features_extractors.AbstractFeaturesExtractor,
               plot: visualisation.PlotClustering):
    name = extractor.__class__.__name__
    features = extractor(htmlpp).tag

    plot.plot_centers(
        f"{name}",
        subtitle=f"{len(features)} tags",
        population=features)


def main(json_file):
    htmlpp = expe_utils.get_htmlpp(json_file)

    extractors = [
        features_extractors.TOIS(),
        features_extractors.LastBlockSemantic(),
        features_extractors.LastBlocksWithComputedStyles(),
    ]

    plot = visualisation.PlotClustering(nrows=3)

    for ext in extractors:
        extraction(htmlpp, ext, plot)

    plot.show()


if __name__ == '__main__':
    json_file = "../../data/html++/calvados.raw.json"
    main(json_file)

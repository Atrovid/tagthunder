import json

import algorithms.experimentations.segmentation.visualisation as visualisation
import algorithms.segmentation.clustering.utils.features_extractors as features_extractors
from algorithms.models.responses import HTMLPP


def get_htmlpp(json_file) -> HTMLPP:
    with open(json_file, "r") as f:
        content = json.load(f)
        htmlpp = HTMLPP(content["html"])

    return htmlpp


def extraction(htmlpp: HTMLPP, extractor: features_extractors.AbstractFeaturesExtractor,
               plot: visualisation.PlotClustering):
    name = extractor.__class__.__name__
    features = extractor(htmlpp).tag

    plot.plot_centers(
        f"{name}",
        subtitle=f"{len(features)} tags",
        population=features)


def main():
    json_file = "../../data/html++/calvados.raw.json"
    htmlpp = get_htmlpp(json_file)

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
    main()

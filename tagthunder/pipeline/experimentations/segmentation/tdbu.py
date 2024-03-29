import pprint

from pipeline.blocks.cleaning import VisionBased
from pipeline.blocks.segmentation import TopDownBottomUp
from pipeline.experimentations.segmentation.visualisation import PlotClustering
from pipeline.models.responses import HTMLPP, Segmentation, HTMLP


def main(htmlpp: HTMLPP):
    algo = TopDownBottomUp()
    segmentation: Segmentation = algo(htmlpp, nb_zones=5)
    return segmentation


def vizu(segmentation):
    plot = PlotClustering(nrows=2)
    plot.plot_centers("TDBU", centers=segmentation.htmlpp)
    plot.show()


if __name__ == '__main__':
    file = "data/example.html"
    with open(file, "r") as f:
        htmlpp = VisionBased()(HTMLP(f))
    segmentation = main(htmlpp)
    pprint.pp(segmentation.zones)

import pipeline.experimentations._utils as expe_utils
from pipeline.blocks.segmentation import TopDownBottomUp
from pipeline.experimentations.segmentation.visualisation import PlotClustering
from pipeline.models.responses import HTMLPP, Segmentation


def main(json_file):
    htmlpp = expe_utils.get_htmlpp(json_file)
    algo = TopDownBottomUp()
    segmentation: Segmentation = algo(htmlpp, nb_zones=5)

    plot = PlotClustering(nrows=2)
    plot.plot_centers("TDBU", centers=segmentation.htmlpp)
    plot.show()


if __name__ == '__main__':
    json_file = "../../data/html++/calvados.raw.json"
    main(json_file)

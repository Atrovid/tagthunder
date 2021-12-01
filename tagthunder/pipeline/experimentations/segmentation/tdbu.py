import pipeline.experimentations._utils as expe_utils
from pipeline.blocks.segmentation import TopDownBottomUp
from pipeline.experimentations.segmentation.visualisation import PlotClustering
from pipeline.models.responses import HTMLPP, Segmentation
from pipeline.models.web_elements import HTMLPPTag


def main(json_file):
    htmlpp = expe_utils.get_htmlpp(json_file)
    algo = TopDownBottomUp()
    segmentation: Segmentation = algo(htmlpp, nb_zones=5)
    sub_segmentation = algo(segmentation.htmlpp[0], nb_zones=5)
    for i, z in enumerate(sub_segmentation.htmlpp):
        print(f'Zone {i}')
        print(z.find_all_visible(recursive=False))
        print()

    plot = PlotClustering(nrows=2)
    plot.plot_centers("TDBU", centers=segmentation.htmlpp)
    plot.plot_centers("", centers=sub_segmentation.htmlpp)
    plot.show()


if __name__ == '__main__':
    json_file = "../../data/html++/calvados.raw.json"
    main(json_file)

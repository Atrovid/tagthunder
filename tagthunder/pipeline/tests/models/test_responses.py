from unittest import TestCase

from pipeline.models.responses import HTMLP, HTMLPP
from pipeline.models.web_elements import HTMLPTag, HTMLPPTag, BoundingBox, CoveringBoundingBox

htmlp_markup = """
    <html><body bbox="0 80 1200 252.875" style="display: block; visibility: visible;" xpath="/html/body"> <div bbox="268 80 664 252.875" style="display: block; visibility: visible;" xpath="/html/body/div"> <h1 bbox="300 133.4375 600 38" style="display: block; visibility: visible;" xpath="/html/body/div/h1">Example Domain</h1> <p bbox="300 192.875 600 57" style="display: block; visibility: visible;" xpath="/html/body/div/p[1]">This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.</p> <p bbox="300 265.875 600 19" style="display: block; visibility: visible;" xpath="/html/body/div/p[2]"><a bbox="300 265.875 152.359375 19" href="https://www.iana.org/domains/example" style="display: inline; visibility: visible;" xpath="/html/body/div/p[2]/a">More information...</a></p> </div> </body></html>
"""


class TestBbox(TestCase):
    def test_bbox(self):
        assert not BoundingBox(0, 0, 0, 0).is_visible
        assert not BoundingBox(0, 0, 10, 0).is_visible
        assert BoundingBox(0, 0, 10, 10).is_visible
        assert BoundingBox(10, 2, 20, 20).is_visible

    def test_covering_bbox(self):
        bboxes = [
            BoundingBox(0, 0, 10, 10),
            BoundingBox(0, 10, 10, 10),
            BoundingBox(10, 0, 10, 10),
            BoundingBox(10, 10, 10, 10)
        ]

        cbbox = CoveringBoundingBox(bboxes)
        desired_corners = [(0, 0), (20, 0), (20, 20), (0, 20)]

        assert all([(c.x, c.y) == p for c, p in zip(cbbox.corners, desired_corners)])
        assert cbbox.area == 10 * 10 * 4
        assert (cbbox.center.x, cbbox.center.y) == (10, 10)


class TestHTMLP(TestCase):
    htmlp = HTMLP(htmlp_markup)

    def test_htmlp_required_attrs(self):
        assert all(
            [
                all([att in tag.attrs for att in (HTMLPTag._BBOX_ATTR, HTMLPTag._STYLES_ATTR, HTMLPTag._XPATH_ATTR)])
                for tag in self.htmlp.html.find_all(True)
            ]
        )

    def test_tags_bbox(self):
        for tag in self.htmlp.html.find_all(True):
            attr = tuple(map(lambda n: int(float(n)), tag.attrs[HTMLPTag._BBOX_ATTR].split(" ")))
            bbox = tag.bbox
            if (bbox.top_left.x, bbox.top_left.y, bbox.width, bbox.height) != attr:
                assert False
            if (bbox.bottom_right.x, bbox.bottom_right.y) != (attr[0] + attr[2], attr[1] + attr[3]):
                assert False

    def test_tags_styles(self):
        for tag in self.htmlp.html.find_all(True):
            if not all([k in tag.styles.keys() for k in ["display", "visibility"]]):
                assert False

    def test_get_comments(self):
        comments = [" C1 ", " C2 ", " C3 "]
        htmlp = HTMLP("""
                    <p>
                        ok
                        <!--{}-->
                        <!--{}-->
                        <p>
                            <!--{}-->
                        </p>
                    </p>
                """.format(*comments))

        assert htmlp.get_comments(False) == []
        assert htmlp.p.get_comments(False) == comments[:2]
        assert htmlp.get_comments(True) == comments


class TestHTMLPP(TestCase):
    htmlpp = HTMLPP(
        """
        <html is-usable="true">
        <body bbox="0 80 1200 252.875" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body">
        <div bbox="268 80 664 252.875" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div">
        <h1 bbox="300 133.4375 600 38" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div/h1">
        Example Domain
        </h1>
        <p bbox="300 192.875 600 57" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div/p[1]">
        This domain is for use in illustrative examples in documents. 
        You may use this domain in literature without prior coordination or asking for permission.</p> 
        <p bbox="300 265.875 600 19" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div/p[2]">
        <a bbox="300 265.875 152.359375 19" href="https://www.iana.org/domains/example" is-usable="true" style="display: inline; visibility: visible;" xpath="/html/body/div/p[2]/a">
        More information...
        </a>
        </p> 
        </div>
        </body>
        </html>
        """
    )

    def test_is_usable(self):
        assert self.htmlpp.html.is_usable

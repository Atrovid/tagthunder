from unittest import TestCase

from pipeline.blocks.cleaning import VisionBased
from pipeline.models.responses import HTMLP
from pipeline.models.web_elements import HTMLPPTag


class TestVisionBased(TestCase):
    control_tags = [
        '<div bbox="300 265.875 0 0" style="display: block; visibility: visible;" xpath="/html/body/div['
        '2]">content</div>',
        '<div bbox="300 265.875 100 100" style="display: none; visibility: visible;">content</div>',
        '<div bbox="300 265.875 100 100" style="display: none; visibility: visible;"></div>',
        '''<div bbox="300 265.875 100 100" style="display: block; visibility: visible;">
            <div bbox="300 265.875 100 100" style="display: none; visibility: visible;"></div>
        </div>''',
        '''<div bbox="300 265.875 100 100" style="display: block; visibility: visible;">
            <div bbox="300 265.875 100 100" style="display: none; visibility: visible;">TEXT</div>
        </div>''',
    ]

    htmlp = HTMLP("""
        <html>
            <body bbox="0 80 1200 252.875" style="display: block; visibility: visible;" xpath="/html/body">
                <div bbox="268 80 664 252.875" style="display: block; visibility: visible;" xpath="/html/body/div"> 
                    <h1 bbox="300 133.4375 600 38" style="display: block; visibility: visible;" xpath="/html/body/div/h1">
                        Example Domain
                    </h1> 
                    <p bbox="300 192.875 600 57" style="display: block; visibility: visible;" xpath="/html/body/div/p[1]">
                        This domain is for use in illustrative examples in documents. 
                        You may use this domain in literature without prior coordination or asking for permission.
                    </p> 
                    <p bbox="300 265.875 600 19" style="display: block; visibility: visible;" xpath="/html/body/div/p[2]">
                        <a bbox="300 265.875 152.359375 19" href="https://www.iana.org/domains/example" style="display: inline; visibility: visible;" xpath="/html/body/div/p[2]/a">
                            More information...
                        </a>
                    </p>
                </div>
                {}{}{}{}{}
            </body>
        </html>
    """.format(*control_tags))
    block = VisionBased()

    def test_remove_comments(self):
        htmlp = HTMLP("""
            <p>
                ok
                <!-- one line comment -->
                <!-- one line comment -->
                <p>
                    <!-- one line comment -->
                </p>
            </p>
        """)
        assert self.block.contains_comment(htmlp)
        self.block.remove_comments(htmlp)
        assert not self.block.contains_comment(htmlp)

        assert not self.block.contains_comment(self.htmlp)
        self.block.remove_comments(self.htmlp)
        assert not self.block.contains_comment(self.htmlp)

    def test_is_useless_tag(self):
        assert all([not self.block.is_useless_tag(tag) for tag in self.htmlp.find_all(True)])

    def test_is_empty_tag(self):
        assert self.block.is_empty_tag(HTMLP(self.control_tags[2]).div)
        assert not self.block.is_empty_tag(HTMLP(self.control_tags[0]).div)
        assert self.block.is_empty_tag(HTMLP(self.control_tags[3]).div)
        assert not self.block.is_empty_tag(HTMLP(self.control_tags[4]).div)

    def test_is_flat_tag(self):
        assert self.block.is_flat_tag(HTMLP(self.control_tags[0]).div)
        assert not self.block.is_flat_tag(HTMLP(self.control_tags[1]).div)

    def test_is_usable_tag(self):
        assert self.block._is_usable_tag(HTMLP(self.control_tags[0]).div)
        assert not self.block._is_usable_tag(HTMLP(self.control_tags[1]).div)

    def test_mark_usable_tag(self):
        tags = [
            (HTMLP("<p style='display: none; visibility: visible;'></p>").p, "false"),
            (HTMLP("<p style='visibility: hidden;'></p>").p, "false"),
            (HTMLP("<p style='display: block;'></p>").p, "true"),
            (HTMLP("<p style='display: inline;'></p>").p, "true"),
        ]

        for t, r in tags:
            self.block.mark_as_usable_tag(t)
            assert t.attrs[HTMLPPTag.IS_USABLE_HTML_ATTR_KEY] == r

    def test_call(self):
        htmlpp = self.block(self.htmlp)
        print(htmlpp.prettify())

from pipeline.models.responses import HTMLP, HTMLPP
from pipeline.models.web_elements import HTMLPTag, HTMLPPTag

htmlp_markup = """
    <html>
    <body bbox="0 80 1200 252.875" style="display: block; visibility: visible;" xpath="/html/body"> 
        <div bbox="268 80 664 252.875" style="display: block; visibility: visible;" xpath="/html/body/div">
            <h1 bbox="300 133.4375 600 38" style="display: block; visibility: visible;" xpath="/html/body/div/h1">Example Domain</h1>
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
    </body>
    </html>
"""


def test_htmlp():
    htmlp = HTMLP(htmlp_markup)

    assert all(
        [
            (HTMLPTag._BBOX_ATTR in tag.attrs, HTMLPTag.styles in tag.attrs)
            for tag in htmlp.find_all(True)
        ]
    )
    print(htmlp.prettify())
    for tag in htmlp.find_all(True):
        print(tag.bbox)

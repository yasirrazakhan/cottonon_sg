import unittest
from pathlib import Path

from scrapy.http import HtmlResponse

from cottonon_sg.spiders.cottonon import CottononSgSpider


class TestSpider(unittest.TestCase):
    def setUp(self):
        with (Path(__file__).parent / "test.html").open("rb") as fh:
            content = fh.read()

        self.resp = HtmlResponse(
            url="https://cottonon.com/SG/textured-short-sleeve-shirt/3610567-07.html",
            body=content,
        )

    def test_product_name(self):
        expected = CottononSgSpider().get_all_product_info(self.resp)
        actual = {
            "title": "Textured Short Sleeve Shirt",
            "variant": "3610567-07",
            "brand": "Cotton On Men",
            "category": "COG SG Megastore Catalog/Men/Shirts",
            "description": "textured cotton short sleeve shirt",
            "images": [
                "https://cottonon.com/dw/image/v2/BBDS_PRD/on/demandware.static/-/Sites-catalog-master-men/default/dw6dfc1000/3610567/3610567-07-2.jpg?sw=104&sh=156&sm=fit",
                "https://cottonon.com/dw/image/v2/BBDS_PRD/on/demandware.static/-/Sites-catalog-master-men/default/dwff04e95b/3610567/3610567-07-1.jpg?sw=104&sh=156&sm=fit",
                "https://cottonon.com/dw/image/v2/BBDS_PRD/on/demandware.static/-/Sites-catalog-master-men/default/dwc25d5002/3610567/3610567-07-3.jpg?sw=104&sh=156&sm=fit",
                "https://cottonon.com/dw/image/v2/BBDS_PRD/on/demandware.static/-/Sites-catalog-master-men/default/dwaa9f21b7/3610567/3610567-07-4.jpg?sw=104&sh=156&sm=fit",
            ],
            "price": "$ 29.99",
            "product_id": "3610567-07",
        }
        self.assertDictEqual(dict(expected), actual)

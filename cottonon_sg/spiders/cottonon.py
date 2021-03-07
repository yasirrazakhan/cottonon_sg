"""There is nice sitemap available which list all the products
https://cottonon.com/SG/sitemap_index.xml"""
from functools import lru_cache
from typing import Dict, Optional, List
import re
import json

from scrapy.spiders import SitemapSpider
from scrapy.responsetypes import Response

from cottonon_sg.items import CottononSgItem


class CottononSgSpider(SitemapSpider):
    name = "cottonon-sg"
    sitemap_urls = ["https://cottonon.com/SG/sitemap_index.xml"]

    # There are other sitemaps as we need to parse the product sitemaps
    sitemap_follow = [r"product"]

    def parse(self, response, **_):
        self.logger.info(f"Found Product Url: {response.url}")
        yield self.get_all_product_info(response)

    def get_all_product_info(self, response: Response) -> CottononSgItem:
        """Return Details for single Product"""
        product = CottononSgItem()
        product["title"] = self.get_product_name(response)
        product["brand"] = self.get_product_brand(response)
        product["price"] = self.get_product_price(response)
        product["description"] = self.get_product_description(response)
        product["images"] = self.get_product_images(response)
        product["category"] = self.get_product_category(response)
        product["product_id"] = self.get_product_id(response)
        product["variant"] = self.get_product_variant(response)
        return product

    @lru_cache()
    def get_product_info(self, response: Response) -> List[Dict]:
        """
        Argument {response}: Html Response of the Product Page
        Returns: {product_info}: List of Dict contains details of a single product
        """

        # Script contains raw info in json format we need to parse it
        raw_info = response.css("script:contains('dataLayerArr')").get("")

        # Compile Regex to make search faster.
        pattern = re.compile(r"{.+}")
        info = re.search(pattern, raw_info)

        if info:
            # Parse the raw json
            product_info = json.loads(info.group())
            return product_info.get("ecommerce").get("detail").get("products", [{}])
        return [{}]

    @lru_cache()
    def get_product_meta(self, response: Response):
        """
        Argument {response}: Html Response of the Product Page
        Returns: {product_meta}: Dict contains product meta for a single product
        """
        product_meta = response.css("#pdpMain::attr(data-bvproduct)").get("")
        # Process raw product_meta json
        data = json.loads(product_meta)
        return data

    def get_product_name(self, response: Response) -> Optional[str]:
        """Parse Product Title"""
        product_name = self.get_product_info(response)[0]
        return product_name.get("name") or None

    def get_product_price(self, response: Response) -> Optional[str]:
        """Parse Product Price"""
        product_price = self.get_product_info(response)[0]
        return f"$ {product_price.get('price')}" or None

    def get_product_category(self, response: Response) -> Optional[str]:
        """Parse Product Category"""
        product_category = self.get_product_info(response)[0]
        return product_category.get("category") or None

    def get_product_variant(self, response: Response) -> Optional[str]:
        """Parse Product Variant"""
        product_variant = self.get_product_info(response)[0]
        return product_variant.get("variant") or None

    def get_product_brand(self, response: Response) -> Optional[str]:
        """Parse Product Brand"""
        product_brand = self.get_product_info(response)[0]
        return product_brand.get("brand") or None

    def get_product_id(self, response) -> Optional[str]:
        """Parse Product Id"""
        product_id = self.get_product_meta(response)
        if product_id:
            return product_id.get("productId")
        return None

    def get_product_description(self, response) -> Optional[str]:
        """Parse Product Description"""
        product_desc = self.get_product_meta(response)
        if product_desc:
            # Remove HTML tags from description info
            pattern = re.compile("<.*?>")
            return re.sub(pattern, "", product_desc.get("productDescription"))
        return None

    def get_product_images(self, response: Response) -> Optional[List]:
        """Parse Product Images"""
        images = response.css(".productthumbnail::attr(src)").getall()
        if images:
            return images
        return None

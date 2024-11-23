
# TODO: CHECK ALL THE TODOs

import scrapy
import json
import re
from pathlib import Path
from dataminer.items import Product  # Replace with your actual items module


# TODO: Rename spider
class PseudoTemplateSpider(scrapy.Spider):
    name = "template_spider"  # Name your spider appropriately

    # TODO: Rename output file and fields:

    custom_settings = {
        'FEEDS': {
            'output/template_products.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'fields': ['id', 'title', 'price', 'approx_price', 'url', 'description'],
            },
        },
    }

    def start_requests(self):
        # Load URLs to start with, modify path as needed

        # TODO: Add URL json-address:

        urls_data = self._load_urls_from_file("../resources/template_urls.json")
        for entry in urls_data:
            url = entry.get('url')
            if url:
                yield scrapy.Request(url=url, callback=self._detect_page_type)

    @staticmethod
    def _load_urls_from_file(file_path):
        """Load URLs from a JSON file."""
        path = Path(__file__).parent / file_path
        with open(path, 'r') as file:
            return json.load(file)

    def _detect_page_type(self, response):
        """Determine if the page is a listing or product page."""


        # TODO: Add logic for detection page type. Remove if not needed.

        if response.css('div.listing-item'):  # Adjust selector based on actual listing container
            self.log("Detected as a listing page.")
            yield from self._parse_listing_page(response)
        elif response.css('h1.product-title'):  # Adjust selector based on actual product title
            self.log("Detected as a product page.")
            yield from self._parse_product(response)

    def _parse_listing_page(self, response):
        """Parse all product URLs on a listing page."""

        # TODO: Add parsing logic:

        product_urls = self._extract_product_urls(response)
        for product_url, product_id in product_urls:
            if product_id:  # Follow only if product_id is found
                yield response.follow(
                    product_url,
                    callback=self._parse_product,
                    meta={'product_url': product_url, 'product_id': product_id}
                )

        # TODO: Add page following logic:

        # Follow next page if available
        next_page = response.css('a.next-page::attr(href)').get()  # Adjust selector for pagination
        if next_page:
            yield response.follow(next_page, callback=self._parse_listing_page)

    @staticmethod
    def _extract_product_urls(response):
        """Extract product URLs and IDs from a listing page."""

        # TODO: Add parsing logic:

        products = []
        for product in response.css('div.listing-item'):  # Adjust selector based on actual listing item
            product_url = product.css('a.product-link::attr(href)').get()  # Adjust selector for product link
            product_id = PseudoTemplateSpider._extract_product_id(product_url)
            if product_url and product_id:
                products.append((product_url, product_id))
        return products

    @staticmethod
    def _extract_product_id(url):
        """Extract product ID from a product URL."""

        # TODO: Add parsing logic:

        match = re.search(r'/itm/(\d+)', url)  # Adjust regex as needed for the site's URL structure
        return match.group(1) if match else None

    def _parse_product(self, response):
        """Parse product details from a product page."""

        # TODO: Add parsing logic:

        product_data = self._extract_product_data(response)
        yield Product(**product_data)

    @staticmethod
    def _extract_product_data(response):
        """Extract structured data for a single product."""

        # TODO: Add parsing logic:

        product_url = response.meta.get('product_url', response.url)
        product_id = response.meta.get('product_id')
        title = response.css('h1.product-title::text').get()  # Adjust selector based on actual product title
        price = response.css('.product-price::text').get() or "0"  # Adjust selector for product price
        approx_price = response.css('.approx-price::text').get()  # Adjust selector if an approx price is available
        description = " ".join(response.css('div.product-description *::text').getall()).strip()  # Adjust selector

        return {
            "id": product_id,
            "title": title,
            "price": price,
            "approx_price": approx_price,
            "url": product_url,
            "description": description
        }

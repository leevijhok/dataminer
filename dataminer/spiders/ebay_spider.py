""" Example ebay spider """

import scrapy
import json
import re
from pathlib import Path
from dataminer.items import Product

class EbaySpider(scrapy.Spider):
    name = "ebay"
    custom_settings = {
        'FEEDS': {
            'output/ebay_products.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'fields': [
                    'id', 'title', 'price', 'approx_price', 'url', 'description'
                ],
            },
        },
    }

    def start_requests(self):
        urls_data = self._load_urls_from_file("../resources/ebay_urls.json")
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
        """Determine whether the page is a listing or product page."""
        if response.css('div.s-item__info'):
            self.log("Detected as a product listing page.")
            yield from self._parse_listing_page(response)
        elif response.css('h1#itemTitle'):
            self.log("Detected as an individual product page.")
            yield from self._parse_product(response)

    def _parse_listing_page(self, response):
        """Parse all product URLs on a listing page."""
        product_urls = self._extract_product_urls(response)
        for product_url, product_id in product_urls:
            if product_id:  # Only follow if product_id is found
                yield response.follow(
                    product_url,
                    callback=self._parse_product,
                    meta={'product_url': product_url, 'product_id': product_id}
                )

        # Follow next page if available
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self._parse_listing_page)

    @staticmethod
    def _extract_product_urls(response):
        """Extract product URLs and IDs from a listing page."""
        products = []
        for product in response.css('div.s-item__info'):
            product_url = product.css('a.s-item__link::attr(href)').get()
            product_id = EbaySpider._extract_product_id(product_url)
            if product_url and product_id:
                products.append((product_url, product_id))
        return products

    @staticmethod
    def _extract_product_id(url):
        """Extract product ID from a product URL."""
        match = re.search(r'/itm/(\d+)', url)
        return match.group(1) if match else None

    def _parse_product(self, response):
        """Parse product details from a product page."""
        product_data = self._extract_product_data(response)
        yield Product(**product_data)

    @staticmethod
    def _extract_product_data(response):
        """Extract and clean data for a single product."""
        product_url = response.meta.get('product_url', response.url)
        product_id = response.meta.get('product_id')
        
        # Basic fields
        title = response.css('[data-testid="x-item-title"] h1.x-item-title__mainTitle span.ux-textspans--BOLD::text').get()
        price = response.css('[data-testid="x-price-primary"]::text').get() or "0"  # Default to "0" if empty
        approx_price = response.css('[data-testid="ux-textual-display"] .ux-textspans--BOLD::text').get()
        description_text = " ".join(response.css('div#viTabs_0_is *::text').getall()).strip()

        # Clean up the URL
        base_url = product_url.split('?')[0]  # Remove query parameters

        # Format and clean approx_price with currency if available
        approx_price_cleaned = approx_price.strip() if approx_price else None

        return {
            "id": product_id,
            "title": title,
            "price": float(price.replace('$', '').replace(',', '').strip()) if price != "0" else None,
            "approx_price": approx_price_cleaned,  # Retain full string with currency
            "url": base_url,
            "description": description_text  # Cleaned description
        }

    @staticmethod
    def _extract_attribute(text, pattern):
        """Extract a single attribute using regex."""
        match = re.search(pattern, text)
        return match.group(1) if match else None

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
from scrapy import Request
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from dataminer.azurehelper import AzureCosmosDBHelper

class AzureCosmosDBPipeline:
    """Pipeline for saving items to Azure Cosmos DB using the helper class."""

    def open_spider(self, spider):
        # Check if Azure integration is enabled from settings
        self.use_azure = spider.settings.getbool('USE_AZURE', False)
        if self.use_azure:
            self.azure_helper = AzureCosmosDBHelper()
            logging.info("AzureCosmosDBPipeline: Initialized Azure helper.")

    def process_item(self, item, spider):
        if self.use_azure:
            try:
                self.azure_helper.upsert_item(dict(item))  # Convert item to dictionary
                logging.info(f"AzureCosmosDBPipeline: Successfully saved item to Azure DB: {item['id']}")
            except Exception as e:
                logging.error(f"AzureCosmosDBPipeline: Error saving item {item['id']} to Azure DB: {e}")
        return item

    def close_spider(self, spider):
        if self.use_azure:
            logging.info("AzureCosmosDBPipeline: Finished processing and closed connection to Azure.")


class CsvExportPipeline:
    """Pipeline placeholder for CSV export settings if additional processing is needed.
       Scrapy's FEEDS handles CSV exports directly based on spider settings."""

    def process_item(self, item, spider):
        # Direct CSV export is handled by Scrapy's FEEDS setting in the spider
        # If additional processing is needed before CSV export, add it here.
        return item

class CustomImagePipeline(ImagesPipeline):
    """Custom image processing pipeline"""

    def get_media_requests(self, item, info):
        if 'image_urls' in item:
            for image_url in item['image_urls']:
                yield Request(image_url)

    def file_path(self, request, response=None, info=None, *, item=None):
        # Save images with a meaningful filename
        return f"images/{item['id']}/{request.url.split('/')[-1]}"

    def item_completed(self, results, item, info):
        # Add downloaded file paths to the item
        item['images'] = [x['path'] for ok, x in results if ok]
        return item

# Future development ideas:    
"""class MLClassificationPipeline:
    def open_spider(self, spider):
        self.model = joblib.load('product_classifier.pkl')

    def process_item(self, item, spider):
        if 'description' in item:
            item['category'] = self.model.predict([item['description']])[0]
        return item"""

# zmq passing pipeline?
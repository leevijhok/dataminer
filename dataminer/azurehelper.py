""" Handles azure-requests """

import os
import logging
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
class AzureCosmosDBHelper:
    def __init__(self):
        # Set up logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Load environment variables
        load_dotenv()
        endpoint = os.getenv("COSMOS_DB_URI")
        key = os.getenv("COSMOS_DB_KEY")
        database_name = os.getenv("DATABASE_NAME")
        container_name = os.getenv("CONTAINER_NAME")

        # Establish connection to Azure Cosmos DB
        try:
            self.client = CosmosClient(endpoint, key)
            self.database = self.client.get_database_client(database_name)
            self.container = self.database.get_container_client(container_name)
            self.logger.info("Successfully connected to Azure Cosmos DB.")
        except Exception as e:
            self.logger.error("Failed to connect to Azure Cosmos DB: %s", e)
            raise

    def upsert_item(self, item):
        """Inserts or updates an item in the Cosmos DB container."""
        try:
            self.container.upsert_item(item)
            self.logger.info(f"Item with ID {item['id']} upserted successfully.")
        except Exception as e:
            self.logger.error(f"Failed to upsert item with ID {item['id']}: %s", e)
            raise

    def delete_item(self, item_id, partition_key):
        """Deletes an item from the Cosmos DB container."""
        try:
            self.container.delete_item(item=item_id, partition_key=partition_key)
            self.logger.info(f"Item with ID {item_id} deleted successfully.")
        except Exception as e:
            self.logger.error(f"Failed to delete item with ID {item_id}: %s", e)
            raise

    def query_items(self, query, parameters=None):
        """Executes a SQL query on the Cosmos DB container."""
        try:
            items = list(self.container.query_items(
                query=query,
                parameters=parameters or [],
                enable_cross_partition_query=True
            ))
            self.logger.info(f"Query returned {len(items)} items.")
            return items
        except Exception as e:
            self.logger.error("Query failed: %s", e)
            raise

    def read_item(self, item_id, partition_key):
        """Reads a single item from the Cosmos DB container."""
        try:
            item = self.container.read_item(item=item_id, partition_key=partition_key)
            self.logger.info(f"Read item with ID {item_id}.")
            return item
        except Exception as e:
            self.logger.error(f"Failed to read item with ID {item_id}: %s", e)
            raise


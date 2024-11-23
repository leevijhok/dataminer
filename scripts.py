"""Wrapper script """
import subprocess
import sys


def start_spider(spider_name, use_azure=False, use_scraperapi=False):
    """
    Wrapper function to run a Scrapy spider with optional flags.

    Args:
        spider_name (str): Name of the spider to run.
        use_azure (bool): Set to True to use Azure Cosmos DB pipeline.
        use_scraperapi (bool): Set to True to use ScraperAPI for proxies.
    """
    # Create the base scrapy command
    command = ["scrapy", "crawl", spider_name]

    # Add flags to the command
    if use_azure:
        command.append("--use-azure")

    if use_scraperapi:
        command.append("--use-scraperapi")
        command += ["--set", "settings=scraperapi_settings"]

    # Execute the command
    subprocess.run(command, check=True)


if __name__ == "__main__":
    # Parse command-line arguments to determine which flags to set
    spider_name = "ebay"  # Default spider name, modify if necessary
    use_azure = "--use-azure" in sys.argv
    use_scraperapi = "--use-scraperapi" in sys.argv

    # Remove flags from sys.argv to prevent duplication
    if "--use-azure" in sys.argv:
        sys.argv.remove("--use-azure")

    if "--use-scraperapi" in sys.argv:
        sys.argv.remove("--use-scraperapi")

    # Start the spider with the appropriate flags
    start_spider(spider_name, use_azure=use_azure, use_scraperapi=use_scraperapi)
""" Settings for the proxy-usage. Is faster. """

from fake_useragent import UserAgent
import random
import sys

# Scrapy settings for dataminer project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "dataminer"

SPIDER_MODULES = ["dataminer.spiders"]
NEWSPIDER_MODULE = "dataminer.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "dataminer (+http://www.yourdomain.com)"
# 
# Random User-Agent rotation
ua = UserAgent()
USER_AGENT = ua.random  # Choose a random user agent

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = random.uniform(0.3, 0.7)
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Enable retries for failed requests
RETRY_TIMES = 5
DOWNLOAD_TIMEOUT = 10

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "dataminer.middlewares.DataminerSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html

# Flag for using ScrapyAPI for proxies:
USE_SCRAPERAPI = '--use-scraperapi' in sys.argv

if USE_SCRAPERAPI:
    sys.argv.remove('--use-scraperapi')

# Flag for using Azure as backend:
USE_AZURE = '--use-azure' in sys.argv

if USE_AZURE:
    sys.argv.remove('--use-azure')

# Running without proxies (Proxymiddleware is empty)
DOWNLOADER_MIDDLEWARES = {
    'dataminer.middlewares.RotateUserAgentMiddleware': 400,
    'dataminer.middlewares.ProxyMiddleware': 410,
    'dataminer.middlewares.CustomRetryMiddleware': 420,
}
    
# Using scrapperapi proxies
if USE_SCRAPERAPI:
    DOWNLOADER_MIDDLEWARES = {
    'dataminer.middlewares.RotateUserAgentMiddleware': 400,
    'dataminer.middlewares.ScraperAPIMiddleware': 410,
    'dataminer.middlewares.CustomRetryMiddleware': 420,
    }

if USE_AZURE:
    DOWNLOADER_MIDDLEWARES['dataminer.middlewares.AzureLoggingMiddleware'] = 430

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#ITEM_PIPELINES = {
#    'dataminer.pipelines.AzureCosmosDBPipeline': 300,  # Azure DB pipeline
#    'dataminer.pipelines.CsvExportPipeline': 400,      # CSV pipeline (final step)
#}

# Define pipelines conditionally
ITEM_PIPELINES = {
    'dataminer.pipelines.CsvExportPipeline': 400
}

# Azure pipeline:
if USE_AZURE:
    ITEM_PIPELINES['dataminer.pipelines.AzureCosmosDBPipeline'] = 300

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"




"""" Manages request/response customization. """

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
import random
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from twisted.internet.error import TimeoutError, DNSLookupError, ConnectionRefusedError
from scrapy.utils.project import get_project_settings
#from dataminer.azurehelper import AzureLoggingHelper  # Optional, if you need Azure logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Custom User-Agent rotation middleware
class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        user_agent_list = crawler.settings.get('USER_AGENT_LIST', [])
        return cls(user_agent_list)

    def process_request(self, request, spider):
        if self.user_agent_list:
            request.headers['User-Agent'] = random.choice(self.user_agent_list)

# Custom Proxy middleware
class ProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        proxy_list = crawler.settings.get('PROXY_LIST', [])
        return cls(proxy_list)

    def process_request(self, request, spider):
        if self.proxy_list:
            proxy = random.choice(self.proxy_list)
            request.meta['proxy'] = proxy

# ScraperAPI Middleware
class ScraperAPIMiddleware:
    def __init__(self):
        settings = get_project_settings()
        self.use_scraperapi = settings.getbool('USE_SCRAPERAPI')
        self.api_key = os.getenv('SCRAPERAPI_KEY')  # Load from .env
        self.base_url = os.getenv('SCRAPERAPI_URL')

        if self.use_scraperapi:
            if not self.api_key:
                raise ValueError("SCRAPERAPI_KEY is not set in the environment variables")
            if not self.base_url:
                raise ValueError("SCRAPERAPI_URL is not set in the environment variables")

            self.scraperapi_url = self.base_url.replace('YOUR_API_KEY', self.api_key)

    def process_request(self, request, spider):
        if self.use_scraperapi:
            # Skip if the request URL is already modified
            if self.scraperapi_url in request.url:
                return

            target_url = request.url
            new_url = f"{self.scraperapi_url}{target_url}"
            spider.logger.info(f"ScraperAPI Middleware: Redirecting request to {new_url}")
            return request.replace(url=new_url)


# Custom Retry Middleware with error handling
class CustomRetryMiddleware(RetryMiddleware):
    EXCEPTIONS_TO_RETRY = (TimeoutError, DNSLookupError, ConnectionRefusedError)

    def __init__(self, settings):
        super().__init__(settings)
        self.max_retries = settings.getint('RETRY_TIMES', 3)

    def process_response(self, request, response, spider):
        # Retry on 500, 503, 504, etc., or when response is not successful
        if response.status in {500, 503, 504, 400, 403}:
            reason = f"{response.status} response"
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        # Retry on specific exceptions
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            return self._retry(request, exception, spider)

# Future development:
"""# Optional: Azure Logging Middleware
class AzureLoggingMiddleware:
    def __init__(self):
        self.azure_logger = AzureLoggingHelper()

    def process_response(self, request, response, spider):
        # Log only certain responses (e.g., errors) to Azure
        if response.status in {500, 503, 504}:
            self.azure_logger.log_error(
                f"Error {response.status} on {request.url} - Retried"
            )
        return response"""


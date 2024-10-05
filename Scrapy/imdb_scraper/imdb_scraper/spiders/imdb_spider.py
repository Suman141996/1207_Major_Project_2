
import scrapy
from scrapy_playwright.page import PageMethod

class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/"]
    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},  
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,  
                    "playwright_page_pagemethod": [
                        PageMethod("wait_for_selector", "li.ipc-metadata-list-summary-item"),
                    ],
                },
                callback=self.parse
            )

    def parse(self, response):
        movies = response.css("li.ipc-metadata-list-summary-item")
        for movie in movies:
            yield{

                "Titles": movie.css("h3::text").get().split(". ")[1],
                "Imdb ratings": movie.css(".ipc-rating-star span::text").get(),
                "Release Year" : movie.css(".cli-title-metadata span::text").get(),
            }

        


import scrapy
from pathlib import Path
import os
from pprint import pprint

class CricbuzzSpider(scrapy.Spider):
    name = "cricbuzz"
    allowed_domains = ["cricbuzz.com"]
    start_urls = ["https://cricbuzz.com"]

    def start_requests(self):
        urls = [
            "https://cricbuzz.com"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2].split('.')[-2]
        print("--------------------------------------")
        data_dir = "\\".join(os.getcwd().split("\\")[:-2]) + '\\data\\'

        # collecting latest news title and urls
        latest_news_data = {}
        latest_news = response.css('a.cb-nws-hdln-ancr')
        for news in latest_news:
            news_url = response.url[:-1]+news.attrib.get('href')  
            news_title = news.attrib.get('title') 
            latest_news_data[news_title] = news_url

        pprint(latest_news_data)
        print("--------------------------------------")
        # filename = f"{data_dir}_latest_news.html"
        # Path(filename).write_bytes(a)
        # self.log(f"Saved file {filename}")

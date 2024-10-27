import scrapy
from pathlib import Path
import os
import json
from pprint import pprint

class CricbuzzSpider(scrapy.Spider):
    name = "cricbuzz"
    allowed_domains = ["cricbuzz.com"]
    start_urls = ["https://cricbuzz.com"]
    latest_news_complete_data = {}

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

        # Fetch responses for additional URLs and pass additional variables
        for latest_news_title in latest_news_data.keys():
            yield scrapy.Request(latest_news_data[latest_news_title], callback=self.parse_news, meta={ 'title_name': latest_news_title})

        # pprint(news_page_response)
        print("--------------------------------------")
        # filename = f"{data_dir}_latest_news.html"
        # Path(filename).write_bytes(a)
        # self.log(f"Saved file {filename}")

    def parse_news(self, response):

        """Parse method for handling responses from news urls."""

        self.logger.info('Processing additional response from %s', response.url)

        # Process the additional response as needed
        article_text_list = response.css('p.cb-nws-para::text').getall()
        article_text = "\n".join(article_text_list)

        # Adding in the complete latest news dictionary
        latest_news_title = response.meta.get('title_name')
        self.latest_news_complete_data[latest_news_title] = article_text
        print("--------------------------------------")
        # print(self.latest_news_complete_data)
        self.save_data()
        print("--------------------------------------")
        # for link in links:
        #     href = link.attrib.get('href')
        #     title = link.attrib.get('title')

    def save_data(self):

        data = {}
        latest_news = []
        for latest_news_title in self.latest_news_complete_data:
            each_news = {}
            each_news['title'] = latest_news_title
            each_news['news'] = self.latest_news_complete_data[latest_news_title]
            latest_news.append(each_news)
        
        data['latest_news_section'] = latest_news

        # Writing JSON data
        file_name = 'data.json'
        data_dir = "\\".join(os.getcwd().split("\\")[:-2]) + '\\data\\' + file_name
        with open(data_dir, 'w') as json_file:
            json.dump(data, json_file, indent=4) 

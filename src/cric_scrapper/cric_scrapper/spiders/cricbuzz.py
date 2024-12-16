import scrapy
import os
import json
import sys
sys.path.append("\\".join(os.getcwd().split("\\")[:-1]))
os.chdir('../../')
import logging
# from src.mongo_script import insert_to_db


class CricbuzzSpider(scrapy.Spider):
    name = "cricbuzz"
    allowed_domains = ["cricbuzz.com"]
    start_urls = ["https://cricbuzz.com"]
    latest_news_complete_data = {}
    match_details = {}


    def start_requests(self):
        urls = [
            "https://cricbuzz.com"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-2].split('.')[-2]
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

        # fetching cricket matches
        cricket_matches_data = {}
        for match in response.css('li.cb-lst-mtch.cb-lst-dom'):
            match_type = match.css('div.cb-mm-typ::text').get()  
            
            # Stop processing if match type is other than INTERNATION
            if match_type != 'INTERNATIONAL' and match_type is not None:
                break  
            
            match_title = match.css('a::attr(title)').get()
            match_url = response.url[:-1] + match.css('a::attr(href)').get()
            cricket_matches_data[match_title] = match_url

        # Fetch responses for additional URLs and pass additional variables
        for cricket_matches_title in cricket_matches_data.keys():
            yield scrapy.Request(cricket_matches_data[cricket_matches_title], callback=self.parse_match_data, meta={ 'title_name': cricket_matches_title})


    def parse_news(self, response):

        """Parse method for handling responses from news urls."""

        self.logger.info('Processing additional response from %s', response.url)

        # Process the additional response as needed
        article_text_list = response.css('p.cb-nws-para::text').getall()
        article_text = "\n".join(article_text_list)

        try:
            # Selecting all text within the table with class 'cb-nws-tbl'
            texts = response.xpath('//table[@class="cb-nws-tbl"]//text()').getall()
            
            # merging all of them in the space separated string so that llm have some context atleast
            cleaned_texts = [text.strip() for text in texts if text.strip()]  
            final_output = ' '.join(cleaned_texts)
            article_text += final_output
        except:
            logging.info("No table found!")

        # Adding in the complete latest news dictionary
        latest_news_title = response.meta.get('title_name')
        self.latest_news_complete_data[latest_news_title] = article_text

    def parse_match_data(self, response):

        """Parse method for handling responses from match urls."""

        self.logger.info('Processing additional response from %s', response.url)

        try:

            # Extracting Series, Venue and Date & Time
            series = response.css('span.text-bold:contains("Series:") + a::attr(title)').get()
            venue = response.css('span.text-bold.pad-left:contains("Venue:") + a::attr(title)').get()
            date_time_parts = response.css('span[itemprop="startDate"] span::text').getall()
            date_time_parts += response.css('span[itemprop="startDate"] span[itemprop="endDate"]::text').getall() 
            date_time = ' '.join(part.strip() for part in date_time_parts if part.strip())
            
            # Creating the result dictionary
            match_details = {
                'Series': series,
                'Venue': venue,
                'Date & Time': date_time,
            }

            # Extracting Bowling Team Score, Batting Team Score, Match Status, Player of the Match and Series
            mini_score_bowling = response.css('div.cb-min-tm.cb-text-gray::text').get()
            mini_score_batting = response.css('div.cb-min-tm:not(.cb-text-gray)::text').get()
            match_status = response.css('div.cb-min-stts.cb-text-complete::text').get()
            player_of_the_match = response.css('div.cb-mom-itm:contains("PLAYER OF THE MATCH") a.cb-link-undrln::text').get()
            player_of_the_series = response.css('div.cb-mom-itm:contains("PLAYER OF THE SERIES") a.cb-link-undrln::text').get()

            # Creating the result dictionary
            match_scores = {
                'Mini Score Bowling': mini_score_bowling,
                'Mini Score Batting': mini_score_batting,
                'Match Status': match_status,
                'Player of the Match': player_of_the_match,
                'Player of the Series': player_of_the_series,
            }

            if None in match_scores.values():
                if match_scores['Match Status'] is None:
                    try:
                        score_div = response.css('div.cb-col.cb-col-67.cb-scrs-wrp')

                        # Loop through each div found and extract text
                        for div in score_div:
                            # Get all text within that div
                            text_content = div.xpath('.//text()').getall()
                            # Clean up the text by stripping whitespace and joining
                            cleaned_text = ' '.join([text.strip() for text in text_content if text.strip()])
                        
                        match_scores['Match Status']=cleaned_text
                    except:
                        if match_scores['Player of the Series'] is None and match_scores['Player of the Match'] is not None:
                            match_scores['Player of the Series'] = "Series is not completed yet."

                        if match_scores['Player of the Series'] is None and match_scores['Player of the Match'] is None and match_scores['Match Status'] is None:
                            match_scores['Match Status'] = "Match is not started yet."
        

            # Complete match details
            match_summary = match_details | match_scores

            # Adding in the complete latest news dictionary
            match_title = response.meta.get('title_name')
            self.match_details[match_title] = match_summary


        except:
            self.log("Skipped ! Due to Error.")

    def close(self, reason):
            self.save_data()


    def save_data(self):

        data = {}
        latest_news = []
        for latest_news_title in self.latest_news_complete_data:
            each_news = {}
            each_news['title'] = latest_news_title
            each_news['news'] = self.latest_news_complete_data[latest_news_title]
            latest_news.append(each_news)
        
        data['latest_news_section'] = latest_news

        match_det = []
        for match in self.match_details:
            each_match = {}
            each_match['title'] = match
            each_match['summary'] = self.match_details[match]
            match_det.append(each_match)
        
        data['match_details'] = match_det

        # Writing JSON data
        # file_name = 'data.json'
        # data_dir = "\\".join(os.getcwd().split("\\")[:-2]) + '\\data\\' + file_name
        # with open(data_dir, 'w') as json_file:
        #     json.dump(data, json_file, indent=4) 

        # insert into db
        # inserted_id = insert_to_db(data)
        # self.log(f"Inserted into db with id:{inserted_id}")

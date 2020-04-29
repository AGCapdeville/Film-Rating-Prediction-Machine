# -*- coding: utf-8 -*-
import scrapy
from items import ImdbItem
from scrapy.crawler import CrawlerProcess

# tag we want = td class="titleColumn"

# xpath = //*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[1]/td[2]/a


class ImdbSpider(scrapy.Spider):
    name = 'imdbspider' # eg name to use when running the script
    allowed_domains = ['imdb.com'] # Let’s say your target url is https://www.example.com/1.html, then add 'example.com' to the list.
    start_urls = ['http://www.imdb.com/chart/top']

    # add this to save file as csv #
    custom_settings = {'FEED_FORMAT':'csv','FEED_URI':'IMDB.csv'}


    def parse(self, response):
        for href in response.css("td.titleColumn a::attr(href)").getall():
            yield response.follow(url=href, callback=self.parse_movie)

    def parse_movie(self, response):
        item = ImdbItem()
        item['title'] = [ x.replace('\xa0', '')  for x in response.css(".title_wrapper h1::text").getall()][0]
        item['directors'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Director")]/following-sibling::a/text()').getall()
        item['writers'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Writers")]/following-sibling::a/text()').getall()
        item['stars'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Stars")]/following-sibling::a/text()').getall()
        item['popularity'] = response.css(".titleReviewBarSubItem span.subText::text")[2].re('([0-9]+)')
        item['rating'] = response.css(".ratingValue span::text").get()

        # TODO, go to next page, if next page is a thing
        return item



# Add this to run everything from this script - just use "sudo python3 imdbSpider"
process = CrawlerProcess() # create instance of CrawlerProcess - This class is the one used by all Scrapy commands
process.crawl(ImdbSpider) # pass this spider class to Scrapy
process.start() # the script will block here until the crawling is finished

""" https://docs.scrapy.org/en/latest/topics/practices.html """
# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ..items import SteamItem
from w3lib.html import remove_tags

class BestsellingSpider(scrapy.Spider):
    name = 'bestselling'
    allowed_domains = ['store.steampowered.com/']
    start_urls = ['http://store.steampowered.com/search/?filter=topsellers/'] 

    def parse(self, response):      
        games = response.xpath("//div[@id='search_resultsRows']/a")

        for game in games:
            loader = ItemLoader(item=SteamItem(), selector= game, response=response)
            loader.add_xpath("game_url", ".//@href") #steam_item['game_url'] = game.xpath(".//@href").get()
            loader.add_xpath("img_url", "div[@class='col search_capsule']/img/@src")
            loader.add_xpath("game_name", ".//span[@class='title']/text()")
            loader.add_xpath("release_date", ".//div[@class='col search_released responsive_secondrow']/text()")
            loader.add_xpath("platforms", ".//span[contains(@class, 'platform_img') or @class='vr_supported']/@class")
            loader.add_xpath("reviews_summary", ".//span[contains(@class, 'search_review_summary')]/@data-tooltip-html")
            loader.add_xpath("discount_rate", ".//div[contains(@class, 'search_discount')]/span/text()")
            loader.add_xpath("original_price", ".//div[contains(@class, 'search_price_discount_combined')]")
            loader.add_xpath("discounted_price", "(.//div[contains(@class, 'search_price discounted')]/text())[2]")                   
            yield loader.load_item()

        next_page = response.xpath("//a[@class='pagebtn' and text()='>']/@href").get()
        if next_page:
            yield scrapy.Request(
                dont_filter= True,
                url = next_page,
                callback = self.parse
            )
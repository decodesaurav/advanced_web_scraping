# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags
from scrapy.selector import Selector

def remove_html(review_summary):
    cleaned_review_summary = ''

    try:
        cleaned_review_summary = remove_tags(review_summary)
    except TypeError:
        cleaned_review_summary = 'No Reviews'
        
    return cleaned_review_summary

def get_platforms(one_class):
    platforms = []

    platform = one_class.split(' ')[-1]
    if platform == 'win':
        platforms.append('windows')
    if platform == 'mac':
        platforms.append('Mac OS')
    if platform == 'linux':
        platforms.append('Linux')
    if platform == 'vr_supported':
        platforms.append('VR Supported')

    return platforms


def get_original_price(html_markup):
    original_price = ''
    selector_obj = Selector(text=html_markup)
    div_with_discount = selector_obj.xpath(".//div[contains(@class, 'search_price discounted')]")
    if len(div_with_discount)>0:
        original_price = div_with_discount.xpath(".//span/strike/text()").get() 
    else:
        original_price = selector_obj.xpath(".//div[contains(@class, 'search_price')]/text()").getall()   
        
    return original_price

def clean_discounted_price(discounted_price):
    if discounted_price:
        return discounted_price.strip()

    return discounted_price 

def clean_discount_rate(disc_rate):
    if disc_rate:
        return disc_rate.lstrip('-')
    return disc_rate   

class SteamItem(scrapy.Item):
    game_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    img_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    game_name = scrapy.Field(
        output_processor = TakeFirst()
    )
    release_date = scrapy.Field(
        output_processor = TakeFirst()
    )
    platforms = scrapy.Field(
        input_processor = MapCompose(get_platforms)
    )
    reviews_summary = scrapy.Field(
        input_processor = MapCompose(remove_html),
        output_processor = TakeFirst()
    )
    original_price = scrapy.Field(
        input_processor = MapCompose(get_original_price, str.strip),
        output_processor = Join('')
    )
    discounted_price = scrapy.Field(
        input_processor = MapCompose(clean_discounted_price),
        output_processor = TakeFirst()
    )
    discount_rate = scrapy.Field(
        input_processor = MapCompose(clean_discount_rate),
        output_processor = TakeFirst()
    )

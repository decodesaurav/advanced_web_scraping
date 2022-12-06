import scrapy
from scrapy.selector import Selector
import json

class ExampleSpider(scrapy.Spider):
    name = 'example'
    def start_requests(self):
        yield scrapy.Request(
            url = 'https://store.steampowered.com/search/results/?query&start=2000&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1',
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'X-Prototype-Version': '1.7'
            },
            callback=self.parse,
            meta= {
                'start': 50
            }
        )
    def parse(self, response):
        resp = json.loads(response.body)
        html = resp.get('results_html')
        html_selector = Selector(text=html)

        current_start = response.meta['start']
        next_start = current_start + 50
        new_url = f"https://store.steampowered.com/search/results/?query&start={next_start}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1"
 
        yield scrapy.Request(
            url = new_url,
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'X-Prototype-Version': '1.7'
            },
            callback=self.parse,
            meta= {
                'start': next_start
            }
        )
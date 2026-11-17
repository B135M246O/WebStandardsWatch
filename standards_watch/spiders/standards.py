from urllib.parse import urlparse

import scrapy
from scrapy.exceptions import CloseSpider

from standards_watch.items import StandardItem


class StandardsSpider(scrapy.Spider):
    name = 'standards'
    allowed_domains = ['www.w3.org']
    start_urls = ['https://www.w3.org/TR/']

    def parse(self, response):
        entries = response.css('.tr-list__item')
        if not entries:
            raise CloseSpider('W3C catalog contains no report cards; check selectors')
        seen = set()
        for entry in entries:
            href = entry.css('h3 a::attr(href)').get()
            name = entry.css('h3 a').xpath('normalize-space(.)').get()
            status = entry.css('.maturity-level').xpath('normalize-space(.)').get()
            published = entry.css('time::attr(datetime)').get()
            if not all((href, name, status, published)):
                raise CloseSpider('Incomplete W3C report card; check selectors')
            url = response.urljoin(href)
            if url in seen:
                continue
            seen.add(url)
            yield StandardItem(
                identifier=urlparse(url).path.rstrip('/').rsplit('/', 1)[-1],
                name=name, status=status, url=url, published=published,
            )

import scrapy


class StandardItem(scrapy.Item):
    identifier = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
    url = scrapy.Field()
    published = scrapy.Field()

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonMobileDetailsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_review = scrapy.Field()
    product_price = scrapy.Field()
    product_image_link = scrapy.Field()
    number_of_review = scrapy.Field()
    delivery_price = scrapy.Field()
    capacity = scrapy.Field()
    type_of_brand = scrapy.Field()
    description = scrapy.Field()

    pass
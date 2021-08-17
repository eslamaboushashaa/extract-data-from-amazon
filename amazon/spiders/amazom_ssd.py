import scrapy
from ..items import AmazonMobileDetailsItem


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    # Crawl Mobiles for top 5 pages

    start_urls = ['https://www.amazon.com/s?k=ssd&page=1']
    # initialize
    page_number = 2

    def parse(self, response):
        #انت عملت الوب دا عشان تطلع كل عنصر من البيانات من الصفحة الاولى مع نظيرتها من الصفحة التانيه
        #this loop to make every type data from first page with the data which i extract from second page in same row
            # all variable here must be in loob
        #items = response.css('div.s-result-item.s-asin.sg-col-0-of-12.sg-col-16-of-20.sg-col.sg-col-12-of-16')
        for item in response.css('div.s-result-item.s-asin.sg-col-0-of-12.sg-col-16-of-20.sg-col.sg-col-12-of-16'):
            product_name = item.css('span.a-size-medium.a-color-base.a-text-normal').css('::text').get()
            product_review = item.css('div.a-row.a-size-small>span>a.a-link-normal>span.a-size-base').css('::text').get()
            product_price = item.css('div.a-row.a-size-base.a-color-base>a>span[data-a-size="l"]>span.a-offscreen').css('::text').get()
            product_image_link = item.css('.s-image::attr(src)').get()
            number_of_review =item.css('div.a-row.a-size-small>span>a.a-link-normal>span.a-size-base::text').get()
            links = item.css('.a-link-normal.a-text-normal::attr(href)').extract()
        #خد بالك هنا من حتة meta  دا هي اللي عملت زي نسخ كدا عشان تقدر تستدعي البيانات من الداله دي في داله تانيه
        #وهتلاقي معلومات عنها لما تبحث عن دالة Request in scrapy
        # Passing it to items dictionary
            for link in links:
                urls = 'https://www.amazon.com'+str(link)
                yield scrapy.Request(response.urljoin(urls), callback=self.parse_page , meta={'product_name':product_name, 'product_review':product_review, 'product_price':product_price, 'product_image_link':product_image_link,'number_of_review': number_of_review})

    # i will make function to parse and extract data which i want from secound
    # in my case i will extaract data about storge ssd disk
    def parse_page(self, response):
        items = AmazonMobileDetailsItem()

        delivery_price = response.css('div#price>table.a-lineitem>tr>td.a-span12>span>span.a-size-base.a-color-secondary::text').getall()
        capacity = response.css('tr.a-spacing-small>td.a-span9>span.a-size-base::text')[0].extract()
        type_of_brand = response.css('tr.a-spacing-small>td.a-span9>span.a-size-base::text')[2].extract()
        description_of_brand = response.css('div#productDescription>p::text').extract()

        items['delivery_price'] = delivery_price
        items['capacity'] = capacity
        items['type_of_brand'] = type_of_brand
        items['description'] = description_of_brand
        items['product_name'] = response.meta['product_name']
        items['product_review'] = response.meta['product_review']
        items['product_price'] = response.meta['product_price']
        items['product_image_link'] = response.meta['product_image_link']
        items['number_of_review'] = response.meta['number_of_review']
        yield items




        # Parse subsequent pages
        next_page = 'https://www.amazon.com/s?k=ssd&page='+ str(AmazonSpiderSpider.page_number)
        if AmazonSpiderSpider.page_number<=3:
            AmazonSpiderSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)

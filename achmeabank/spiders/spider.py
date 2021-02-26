import scrapy

from scrapy.loader import ItemLoader
from ..items import AchmeabankItem
from itemloaders.processors import TakeFirst


class AchmeabankSpider(scrapy.Spider):
	name = 'achmeabank'
	start_urls = ['https://www.achmeabank.com/news']

	def parse(self, response):
		post_links = response.xpath('//div[@class="large-4 medium-6 columns itemcontainer"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="medium-12 columns text-center"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//ul[@class="blocks"]//text()[normalize-space() and not(ancestor::a[@class="button hollow"] | ancestor::footer)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="content medium-10"]/p/text()').getall()
		date = [p.strip() for p in date]
		date = ' '.join(date).strip()

		item = ItemLoader(item=AchmeabankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

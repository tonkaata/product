import scrapy
import json
from ..items import ProductItem

class ProductSpider(scrapy.Spider):
	name = 'product'
	start_urls = ['https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99']

	headers = {
		"accept": "application/json, text/plain, */*",
		"accept-encoding": "gzip, deflate, br",
		"accept-language": "en-US,en;q=0.9",
		"cache-control": "no-cache",
		"pragma": "no-cache",
		"referer": "https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99",
		"sec-ch-ua-mobile": "?0",
		"sec-ch-ua-platform": '"Windows"',
		"sec-fetch-dest": "empty",
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "same-origin",
		"stock-id": "006.IN.0.false.false.v0",
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
	}

	def parse(self, response):
		url = 'https://shop.mango.com/services/garments/1704202099'
		yield scrapy.Request(url,callback=self.parse_api, headers=self.headers)

	def parse_api(self,response):
		allData = json.loads(response.body)
		productData = ProductItem()
		colorID = self.start_urls[0].split('c=')[1] if 'c=' in self.start_urls[0] else allData["colors"]["colors"][0]["id"]
		pickedColorData = [a for a in allData["colors"]["colors"] if a["id"] == colorID][0]

		productData['name'] = allData["name"]
		productData['price'] = allData["price"]["price"]
		#output['price'] = pickedColorData["price"] #this is in case price needed per color
		productData['color'] = pickedColorData["label"]
		productData['size'] = [a["value"] for a in pickedColorData["sizes"]][1:]
		#productData['size'] = [a["value"] for a in pickedColorData["sizes"] if 'available' in a.keys()]#In case only available sizes needed

		yield productData #productdata.json file exported via pipelines.py



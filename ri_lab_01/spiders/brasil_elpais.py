# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem

months = {'JAN': '1', 'FEB': '2', 'MAR': '3', 'ABR': '4', 'MAI': '5', 'JUN': '6', 'JUL': '7', 'AGO': '8', 'SET': '9', 'OUT': '10', 'NOV': '11', 'DEZ': '12'}

class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = []

    def __init__(self, *a, **kw):
        super(BrasilElpaisSpider, self).__init__(*a, **kw)
        with open('seeds/brasil_elpais.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())
    
    def parse_page(self, response):
		def extract_with_css(query):
			return response.css(query).get(default='').strip()
		
		def extract_with_css_list(query):
			return " ".join(quote for quote in response.css(query).getall())
		
		def format_date(date_str):
			res = date_str.split()
			res = res[0]+ "/" + months[res[1]]+ "/" + res[2] + " " + res[4]
			return res
			
		yield {
			'title': extract_with_css('h1.articulo-titulo::text'),
			'sub_title': extract_with_css('h2.articulo-subtitulo::text'),
			'author': extract_with_css('span.autor-nombre a::text'),
			'date': format_date(extract_with_css('time a::text')),
			'section': extract_with_css('div.seccion-migas a span::text'),
			'text': extract_with_css_list('div.articulo-cuerpo p::text'),
			'url': response.url
		}	

    def parse(self, response):
		for href in response.css('h2.articulo-titulo a::attr(href)').getall()[:20]:
			yield response.follow(href, callback=self.parse_page)


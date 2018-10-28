# -*- coding: utf-8 -*-
import scrapy


class ReportsSpider(scrapy.Spider):
    name = 'reports'
    base_url = 'https://www.berlin.de'
    start_urls = ['https://www.berlin.de/polizei/polizeimeldungen/archiv/']

    def parse(self, response):
        for archive in response.css('.column-content .textile > ul > li > a'):
            url = self.base_url + archive.css('::attr(href)').extract_first()

            yield scrapy.Request(url=url, callback=self.parse_archive)

    def parse_archive(self, response):

        print(response.url)

        for report_link in response.css('.list-autoteaser > li a'):
            url = self.base_url + report_link.css('::attr(href)').extract_first()
            print(url)



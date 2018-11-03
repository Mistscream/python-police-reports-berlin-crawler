# -*- coding: utf-8 -*-
import scrapy

from police_reports_berlin.items import PoliceReportBerlinItem


# noinspection PyMethodMayBeStatic
class ReportsSpider(scrapy.Spider):
    name = 'reports'
    base_url = 'https://www.berlin.de'
    start_urls = ['https://www.berlin.de/polizei/polizeimeldungen/archiv/']

    def parse(self, response):
        for archive in response.css('.column-content .textile > ul > li > a'):
            url = self.base_url + archive.css('::attr(href)').extract_first()

            yield scrapy.Request(url=url, callback=self.parse_archive)

    def parse_archive(self, response):
        for report_link in response.css('.list-autoteaser > li a'):
            url = self.base_url + report_link.css('::attr(href)').extract_first()

            yield scrapy.Request(url=url, callback=self.parse_report)

    def parse_report(self, response):
        texts = None
        for p in response.css('.column-content .textile p'):
            texts = p.css('::text').extract()
            texts = [text.replace('\n', '').strip() for text in texts]
            texts = list(filter(None, texts))

        report = PoliceReportBerlinItem(
            raw=response.text,
            url=response.url,
            text='. '.join(texts)
        )

        yield report

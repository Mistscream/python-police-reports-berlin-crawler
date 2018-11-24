# -*- coding: utf-8 -*-
import logging
from datetime import datetime

import scrapy
from toolz.curried import pipe, map, filter
from police_reports_berlin.items import PoliceReportBerlinItem

logger = logging.getLogger()


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
        for report in response.css('.list-autoteaser > li.row-fluid'):
            timestamp = report.css('.date::text').extract_first()
            category = report.css('.category::text').extract_first()

            url = self.base_url + report.css('a::attr(href)').extract_first()

            yield scrapy.Request(
                url=url,
                callback=self.parse_report,
                meta={'timestamp': timestamp, 'category': category}
            )

        next_page_url = response.css('.html5-nav > div > ul > .pager-item-next > a::attr(href)').extract_first()

        if next_page_url:
            next_page_url = self.base_url + next_page_url
            yield scrapy.Request(url=next_page_url, callback=self.parse_archive)

    def parse_report(self, response):
        timestamp = response.meta['timestamp']
        timestamp = timestamp.replace('Uhr', '').strip()
        timestamp = datetime.strptime(timestamp, '%d.%m.%Y %H:%M')
        category = response.meta['category']

        title = response.css('.html5-header > .title::text').extract_first()

        snippets = pipe(
            response.css(
                '.column-content > .article > .body .polizeimeldung::text,' +
                '.column-content > .article > .body p::text,' +
                '.column-content > .article > .body strong::text'
            ).extract(),

            map(lambda snippet: snippet.replace('\n', '')),
            map(lambda snippet: snippet.strip()),
            filter(None),

            list
        )

        text = '. '.join(snippets)

        report = PoliceReportBerlinItem(
            category=category,
            timestamp=timestamp,
            title=title,
            url=response.url,
            text=text
        )

        yield report

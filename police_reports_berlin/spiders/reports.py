# -*- coding: utf-8 -*-
import logging
from datetime import datetime

import scrapy
from scrapy.selector import Selector
from toolz.curried import pipe, map, filter
import w3lib.html
import re

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
        timestamp = response.meta['timestamp'] if 'timestamp' in response.meta.keys() else None
        timestamp = timestamp.replace('Uhr', '').strip() if timestamp else None
        timestamp = datetime.strptime(timestamp, '%d.%m.%Y %H:%M') if timestamp else ''
        category = response.meta['category'] if 'category' in response.meta.keys() else ''
        category = category.replace(' - ', '-').replace(' -', '-').replace('- ', '-').strip() if category else ''

        title = response.css('.html5-header > .title::text').extract_first()

        text1 = re.sub(
            ' +', ' ',
            pipe(
                response.css(
                    '.column-content > .article > .body span::text,' +
                    '.column-content > .article > .body p::text'
                ).extract(),
                map(lambda snippet: snippet.replace('\n', ' ')),
                filter(lambda snippet: snippet.replace('\n', '').strip() != ''),

                list,
                ''.join
            ).strip()
        )

        text2 = re.sub(
            ' +', ' ',
            pipe(
                response.css(
                    '.column-content > .article > .body'
                ).extract(),
                map(lambda tag: w3lib.html.remove_tags(tag, keep=('div', 'p'))),
                map(lambda tag: w3lib.html.replace_tags(tag, ' ')),
                map(lambda snippet: snippet.replace('\n', ' ')),
                filter(lambda snippet: snippet.replace('\n', '').strip() != ''),

                list,
                ''.join
            ).strip()
        )

        report = PoliceReportBerlinItem(
            category=category,
            timestamp=timestamp,
            title=title,
            url=response.url,
            text1=text1,
            text2=text2
        )

        yield report

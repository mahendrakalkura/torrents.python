# -*- coding: utf-8 -*-

from grequests import get, map
from scrapy import Selector
from terminaltables import AsciiTable

items = {}

for response in map(
    (
        get(url)
        for url in [
            'http://thepiratebay.co.in/recent/{page}'.format(page=page)
            for page in range(0, 29)
        ] + [
            'http://thepiratebay.co.in/top/48h200',
            'http://thepiratebay.co.in/top/48h500',
        ]
    )
):
    selector = Selector(text=response.text)
    for tr in selector.xpath('//table[@id="searchResult"]/tr'):
        if len(tr.xpath('./td')) != 4:
            continue
        a = tr.xpath('./td[1]')[0].xpath('string()').extract()[0].strip().replace('\n', ' - ')
        b = tr.xpath('./td[3]').xpath('string()').extract()[0].strip()
        if int(b) <= 99:
            continue
        c = tr.xpath('./td[2]/div/a/text()').extract()[0].strip().replace('\n', ' - ')
        d = 'http://thepiratebay.co.in{path}'.format(path=tr.xpath('./td[2]/div/a/@href').extract()[0].strip())
        if c not in items:
            items[c] = [a, b, c, d]
        else:
            if b > items[c][2]:
                items[c] = [a, b, c, d]

print AsciiTable(
    [['Category', 'Seeds', 'Title', 'URL']] +
    sorted(items.values(), key=lambda item: (item[0], -int(item[1]), item[2]))
).table

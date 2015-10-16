import scrapy
from TextMining.items import TextminingItem
from urlparse import urlparse
from urlparse import urljoin

class TextMiningSpider(scrapy.Spider):
    name = "phisan"
    allowed_domains = [
        "phisan.sskru.ac.th",
        "health.kapook.com",
        "frynn.com",
        "rspg.or.th",
    ]

    start_urls = [
        "http://health.kapook.com/herb",
        "http://frynn.com/herb",
        "http://frynn.com/%e0%b8%a3%e0%b8%b2%e0%b8%a2%e0%b8%8a%e0%b8%b7%e0%b9%88%e0%b8%ad%e0%b8%aa%e0%b8%a1%e0%b8%b8%e0%b8%99%e0%b9%84%e0%b8%9e%e0%b8%a3",
        'http://www.rspg.or.th/plants_data/herbs/herbs_200.htm',
    ]

    def parse(self, response):
        selectors = [
            '//ul/li',
            '//ol/li',
            '//tr/td',
            '//div',
            '//p',
            '//font'
        ]
        for selector in selectors:
            for sel in response.xpath(selector):
                item = TextminingItem()
                titles = sel.xpath('a/text()').extract()
                links = sel.xpath('a/@href').extract()

                # for multiple links
                if len(links) != 0:
                    index = 0
                    for link in links:
                        item['link'] = link
                        r = urlparse(link)
                        item['netloc'] = r[1]

                        if len(titles) != 0:
                            item['title'] = titles[index]
                        else:
                            item['title'] = titles

                        # for relative path link
                        if item['netloc'] == '':
                            item['link'] = urljoin(response.url, link)
                            r = urlparse(item['link'])
                            item['netloc'] = r[1]

                        index += 1
                        yield item











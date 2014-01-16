from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

from ..items import LivejournalItem


class LiveJournalSpider(CrawlSpider):
    name = "livejournal"
    allowed_domains = []
    g_ = open('id_lists.dat', 'r')
    start_urls = []
    for e in g_:
        start_urls.append('http://www.' + e.strip() + '.livejournal.com/profile')


    def parse(self, response):
        self.log('Hi, this is: %s' % response.url)
        hxs = HtmlXPathSelector(response)

        nomore = False

        try:
            more_url = (hxs.select('//a[@class = "b-friendslist-more"]/@href').extract())[0].decode('utf-8')
        except:
            nomore = True

        if nomore == True:
            item = LivejournalItem()
            item['url'] = response.url
            # item['_id'] = self.get_username(response.url)
            item['pname'] = self.get_username(response.url)
            item['friend'] = []
            item['friend'].append(hxs.select('//a[@class = " b-profile-username  "]/text()').extract())
            print item['pname'],item['friend']
            yield item
        else:
            url = more_url
            yield Request(url, callback=self.parse)


    def get_username(self, url):
        x = url.split(".")[0].split("//")[1]
        return x


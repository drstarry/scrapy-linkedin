from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

# from ..items import LivejouralItem


class LiveJournalSpider(CrawlSpider):
    name = "livejournal"
    allowed_domains = []
    g_ = open('id_lists.dat', 'r')
    start_urls = []
    for e in g_:
        start_urls.append('http://www.' + e.strip() + '.livejournal.com/profile')

    # rules = (Rule(SgmlLinkExtractor(allow=[r'/people/.*/contacts/\?filter=.*']),callback='parse'),)

    def parse(self, response):
        self.log('Hi, this is: %s' % response.url)
        hxs = HtmlXPathSelector(response)

        nomore = False

        try:
            more_url = (hxs.select('//a[@class = "b-friendslist-more"]/@href').extract())[0].decode('utf-8')
        except:
            nomore = True

        if nomore == True:
            url = response.url
            # item = LiveJouralItem()
            # item['_id'] = self.get_username(response.url)
            # item['pname'] = item["_id"]
            # item['friend'] = []
            friend = []
            friend.append(hxs.select('//div[@class="b-tabs-content"]/a[@class = "b-profile-username"]/text()').extract())
            print friend
            # yield item
        else:
            url = more_url
            yield Request(url, callback=self.parse)


    # def get_username(self, url):
    #     find_index = url.find("livejournal.com/people/")
    #     if find_index >= 0:
    #         x = url[find_index:].split("/")
    #         return x[2]
    #     return None

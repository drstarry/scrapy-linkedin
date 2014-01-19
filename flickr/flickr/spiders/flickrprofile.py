from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

from ..items import FlickrProfileItem


class FlickrprofileSpider(CrawlSpider):
    name = "flickrprofile"
    allowed_domains = []
    g_ = open('id_lists.dat', 'r')
    start_urls = []
    for e in g_:
        start_urls.append('http://www.Flickr.com/people/' + e.strip())

    def parse(self, response):
        self.log('Hi, this is: %s' % response.url)
        hxs = HtmlXPathSelector(response)
        dls = hxs.select('//div[@id = "a-bit-more-about"]/dl')

        # item = FlickrProfileItem()
        # item['_id'] = self.get_username(response.url)
        _id = self.get_username(response.url)
        print _id

        for dl in dls:
            if dl.select('dt/text()').extract()[0] == "Name:":
                try:
                    given_name = dl.select('dd/span[@class="given-name"]/text()').extract()[0]
                except:
                    pass
                else:
                    print 'given_name:',given_name
                    # item['given_name'] = given_name

                try:
                    family_name = dl.select('dd/span[@class = "family-name"]/text()').extract()[0]
                except:
                    pass
                else:
                    print 'family_name:',family_name
                    # item['family_name'] = family_name

            if dl.select('dt/text()').extract()[0] == "Joined:":
                joined = dl.select('dd/text()').extract()[0]
                print 'joined time:',joined
                #item['joined'] = joined

            if dl.select('dt/text()').extract()[0] == "Hometown:":
                home = dl.select('dd/text()').extract()[0]
                print 'hometown:',home
                #item['home'] = home

            if dl.select('dt/text()').extract()[0] == "Currently:":
                try:
                    locality = dl.select('dd/span[@class = "adr"]/span[@class = "locality"]/text()').extract()[0]
                except:
                    pass
                else:
                    print 'locality:',locality
                    #item['locality'] = locality

                try:
                    country_name = dl.select('dd/span[@class = "adr"]/span[@class = "country-name"]/text()').extract()[0]
                except:
                    pass
                else:
                    print 'country-name:',country_name
                    #item['country_name'] = country-name

            if dl.select('dt/text()').extract()[0] == "I am:":
                gender = dl.select('dd/text()').extract()[0]
                print 'gender:',gender
                #item['gender'] = gender

            if dl.select('dt/text()').extract()[0] == "Occupation:":
                occupation = dl.select('dd/text()').extract()[0]
                print 'occupation:',occupation
                #item['occupation'] = occupation

            if dl.select('dt/text()').extract()[0] == "Website:":
                websitename = dl.select('dd/a/text()').extract()[0]
                websiteurl = dl.select('dd/a/@href').extract()[0]
                print 'website:',websitename,websiteurl
                #item['websitename'] = websitename
                #item['websiteurl'] = websiteurl


        # yield item


    def get_username(self, url):
        find_index = url.find("Flickr.com/people/")
        if find_index >= 0:
            x = url[find_index:].split("/")
            return x[2]
        return None

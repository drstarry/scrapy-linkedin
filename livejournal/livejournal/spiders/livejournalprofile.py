from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

# from ..items import LivejournalprofileItem


class LiveJournalprofileSpider(CrawlSpider):
    name = "livejournalprofile"
    allowed_domains = []
    g_ = open('id_lists.dat', 'r')
    start_urls = []
    for e in g_:
        start_urls.append('http://www.' + e.strip() + '.livejournal.com/profile/')


    def parse(self, response):
        self.log('Hi, this is: %s' % response.url)
        hxs = HtmlXPathSelector(response)

        nomore = False

        dts = hxs.select('//dl[@class = "b-profile-group b-profile-userinfo"]/dt/text()').extract()
        # print dts
        dds = hxs.select('//dl[@class = "b-profile-group b-profile-userinfo"]/dd')

        # item = LivejournalprofileItem()
        # item['_id'] = self.get_username(response.url)
        print 'id:',self.get_username(response.url)

        for x,dt in enumerate(dts):
            if dt == "Name:":
                name = dds[x].select('text()').extract()
                print 'name:',name
                # item['name'] = name

            if dt == "Birthdate:":
                birthday = dds[x].select('text()').extract()
                print 'birthday:',birthday
                # item['birthday'] = birthday

            if dt == "Location:":
                try:
                    locality = dds[x].select('a[@class = "locality"]/text()').extract()
                except:
                    pass
                else:
                    print 'Locality:',locality
                    # item['locality'] = locality

                try:
                    country_name = dds[x].select('a[@class = "country-name"]/text()').extract()
                except:
                    pass
                else:
                    print 'country_name:',country_name
                    # item['country_name'] = country_name

            if dt == "Website:".encode("utf-8"):
                website = dds[x].select('a/text()').extract()
                print 'website:',website
                # item['website'] = website

            if dt == "External Services:":
                # item['contacts'] = []
                contacts = []
                try:

                    mailname = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-mail"]/*/span/a/text()').extract()[0]
                    mailurl = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-mail"]/span[2]/span/a/@href').extract()[0]
                    print 'mail:',mailname,mailurl
                except:
                    print '~'
                    pass
                else:
                    contacts.append({"mailname":mailname,"mailurl":mailurl})

                try:
                    twittername = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-twitter"]/a/text()').extract()
                    twitterurl = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-twitter"]/a/@href').extract()
                    print 'twitter:',twittername,twitterurl
                except:
                    pass
                else:
                    contacts.append({"twittername":twittername,"twitterurl":twitterurl})

                try:
                    vkname = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-vk"]/a/text()').extract()
                    vkurl = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-vk"]/a/@href').extract()
                    print 'vk:',vkname,vkurl
                except:
                    pass
                else:
                    contacts.append({"vkname":vkname,"vkurl":vkurl})

                try:
                    ljtname = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-ljtalk"]/span/a/text()').extract()
                    ljturl = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-ljtalk"]/span/a/@href').extract()
                    print 'ljt:',ljtname,ljturl
                except:
                    pass
                else:
                    contacts.append({"ljtname":ljtname,"ljturl":ljturl})


                try:
                    icqname = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-icq"]/a/text()').extract()
                    icqurl = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-icq"]/a/@href').extract()
                    # print 'icq:',icqname,icqurl
                except:
                    pass
                else:
                    contacts.append({"icqname":icqname,"icqurl":icqurl})

                try:
                    yhname = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-yahoo"]/a/text()').extract()
                    yhurl = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-yahoo"]/a/@href').extract()
                    # print 'yahoo:',yhname,yhurl
                except:
                    pass
                else:
                    contacts.append({"yahooname":yhname,"icqurl":yhurl})

                try:
                    gname = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-google"]/text()').extract()
                    # print 'google:',gname
                except:
                    pass
                else:
                    contacts.append({"google":"gtalk","googlename":gname})

                try:
                    skype = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-skype"]/text()').extract()
                    # print 'skype:',skype
                except:
                    pass
                else:
                    contacts.append({"skype":"skype","skype":skype})

                try:
                    lastfmname = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-yahoo"]/a/text()').extract()
                    lastfmurl = dds[x].select('ul/li[@class = "b-contacts-item b-contacts-yahoo"]/a/@href').extract()
                    # print 'lastfm:',lastfmname,lastfmurl
                except:
                    pass
                else:
                    contacts.append({"lastfmname":lastfmname,"lastfmurl":lastfmurl})
                print contacts

                # item['contacts'] = contacts

            if dt == "Schools:":
                schools = dds[x].select('//div/text()').extract()
                # print 'schools:',schools
                # item['schools'] = schools

        bio = hxs.select('//dd[@class = "b-profile-group-body b-collapse-content"]').extract()
        # print bio
        # item['bio'] = bio
        # yield item



    def get_username(self, url):
        x = url.split(".")[0].split("//")[1]
        return x


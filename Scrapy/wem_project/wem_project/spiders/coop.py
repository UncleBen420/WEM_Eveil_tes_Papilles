import json
import scrapy
from unidecode import unidecode

class CoopSpider(scrapy.Spider):
    name = "coop"
    # vin rouge
    #base_url = "https://www.coop.ch/fr/vins/assortiment-de-vin/vins-rouges/"
    # vin blanc
    base_url = "https://www.coop.ch/fr/vins/assortiment-de-vin/vins-blancs/"

    start_urls = [
        #vin rouge
        #base_url + 'c/m_0223',
        #vin blanc
        base_url + 'c/m_0235',
    ]

    def parse(self, response):
        data = json.loads(response.xpath('//script[@type="application/ld+json"]')[1].css('::text').get())

        for w in data['itemListElement']:
            url = self.base_url + w['url'].rsplit("/")[-3] + '/' + w['url'].rsplit("/")[-2] + '/' + w['url'].rsplit("/")[-1]

            to_pass = {
                    "link": url
                }

            yield response.follow(url, callback=self.parse_wine, cb_kwargs=to_pass)

        pagination_links = response.css('a.pagination__next')

        yield from response.follow_all(pagination_links, self.parse)

    def parse_wine(self, response, link):

        title = unidecode(response.css('title::text').get()).replace(" acheter a prix reduit | coop.ch", "")
        description = unidecode(response.css('p.productDescription::text').get())

        pairsWellWith = []
        for r in response.css('.productCharacteristics__content-row'):
            children = r.xpath("./*")
            if children[0].css('div::text').get().strip() == "Idéal avec:":
                pairsWellWith_unprocessed = children[1].css('div::text').get().strip().lower().split(", ")
                pairsWellWith = []
                for food in pairsWellWith_unprocessed:
                    pairsWellWith.append(unidecode(food))
            elif children[0].css('div::text').get().strip() == "Pays:":
                country = unidecode(children[1].css('a::text').get().strip().lower())
            elif children[0].css('div::text').get().strip() == "Cépage:":
                grape_variety = unidecode(children[1].css('a::text').get().strip().lower())

        print("-----------------")
        print(title)
        print(link)
        print(country)
        print(grape_variety)
        print(description)
        print(pairsWellWith)
        print("-----------------")

        yield {
            'title': title,
            'link': link,
            'country': country,
            'grape_variety': grape_variety,
            'description':description,
            'pairsWellWith': pairsWellWith
        }

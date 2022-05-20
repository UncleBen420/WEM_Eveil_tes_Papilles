import scrapy
from unidecode import unidecode
import re
import numpy as np


class MondoVinoSpider(scrapy.Spider):
    name = "mondovino"

    def start_requests(self):
        url = 'http://www.mondovino.com/3-appellations-bordeaux'
        arg_next ={"page_number":1}
        yield scrapy.Request(url, self.parse, cb_kwargs=arg_next)

    # Parse les page interne pour obtenir plus d'information sur les documents
    def parse_inner_page(self, response, title, link):

        price = re.sub(r'[^A-Za-z0-9.]+', '', response.css("div.our_price_display::text").get().replace(',','.'))

        dict_infos = {}
        # pour chaque champ dans la description
        for field in response.css("div.semi-col>p"):

            # récupération de la clé
            key = field.css("strong::text").get()
            # certaines clés retourne des null il faut donc le verifier
            if key:

                # cast de la clé
                key = unidecode(key).replace(" :", "").rstrip().lower()

                # le champ description n'a pas de clé mais séparé en plusieurs partie, il faut donc verifier le nombre de valeurs
                value = field.xpath('./text()').getall()
                if len(value) == 1:

                    value = value[0]
                    # certaines valeurs ont des parties séparées dans des balises span
                    value2 = field.css("span::text").get()

                    if value:
                        value = unidecode(value)
                    else:
                        value = ""

                    if value2:
                        value2 = unidecode(value2)
                    else:
                        value2 = ""

                    value = value + value2

                    dict_infos[key] = value

                # si il y a plusieurs parties on sait qu'il s'agit de la description
                elif len(value) >= 2:

                    value = unidecode(value[0]) + key + unidecode(value[1])

                    dict_infos["description"] = value

        yield {
            'title':title,
            'link':link,
            'price':price,
            'infos':dict_infos
        }

    # parse les pages principale et appel la fonction des inner page
    def parse(self, response, page_number):

        vines = response.css('div.visuel > a')
        if vines:
            for vine in vines:
                title = unidecode(vine.attrib['title'])
                link = unidecode(vine.attrib['href'])

                to_pass = {
                    "title": title,
                    "link" : link
                }
                # pour chaque article va dans la page associée
                yield response.follow(link, callback=self.parse_inner_page, cb_kwargs = to_pass)

            page_number += 1
            arg_next ={"page_number":page_number}
            url = 'http://www.mondovino.com/3-appellations-bordeaux?p=' + str(page_number)

            yield scrapy.Request(url, self.parse, cb_kwargs=arg_next)

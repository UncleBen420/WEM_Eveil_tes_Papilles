import scrapy
from unidecode import unidecode
import re


class MarmitonSpider(scrapy.Spider):
    name = "marmiton"

    def start_requests(self):
        # plat principaux
        #url = 'https://www.marmiton.org/recettes/index/categorie/plat-principal'
        # dessert
        #url = 'https://www.marmiton.org/recettes/index/categorie/dessert'
        # entree
        url = 'https://www.marmiton.org/recettes/index/categorie/entree'
        arg_next ={"page_number":1,
                    "url":url}
        yield scrapy.Request(url + '?rcp=0', self.parse, cb_kwargs=arg_next)

    # Parse les page interne pour obtenir plus d'information sur les documents
    def parse_inner_page(self, response, title, link, image_link, duration, score):

        nb_people = response.css('span.SHRD__sc-w4kph7-4.hYSrSW::text').get()

        ingredients = response.css('div.RCP__sc-vgpd2s-1.fLWRho')
        ingr_array = []
        for ingredient in ingredients:
            temp = ingredient.css('span.SHRD__sc-10plygc-0.epviYI::text').getall()

            if len(temp) == 0:
                quantity = -1
                unit = "None"

            elif len(temp) > 1:
                quantity = unidecode(temp[0])
                unit = unidecode(temp[-1])
            else:
                quantity = unidecode(temp[0])
                unit = "piece"

            ingr = unidecode(ingredient.css('span.RCP__sc-8cqrvd-3::text').get())
            ingr_array.append({"quantity":quantity, "unit":unit, "ingredient": ingr})

        if len(ingr_array) == 0:
            type = "tips"
        else:
            #type = "plat"
            type = "entree"
            #type = "dessert"

        steps = response.css('p.RCP__sc-1wtzf9a-3.jFIVDw::text').getall()
        steps_clean = ""
        for step in steps:
            splited = unidecode(step).split(".")
            for splits in splited:
            	steps_clean = steps_clean + splits + ' '

        steps_clean =  " ".join(steps_clean.split())
        #steps_clean = steps_clean.rstrip(steps_clean[-1])


        yield {
            'title':title,
            'image_link':image_link,
            'link':link,
            'duration':duration,
            'score':score,
            'ingredients':ingr_array,
            'steps':steps_clean,
            'nb_people': nb_people,
            'type': type
        }

    # parse les pages principale et appel la fonction des inner page
    def parse(self, response, page_number, url):

        articles = response.css('div.recipe-card > a')
        if articles:
            for article in articles:
                title = unidecode(article.css('h4::text').get())
                link = article.attrib['href']
                image_link = article.css('img').attrib["data-src"]
                duration = article.css('span.recipe-card__duration__value::text').get()
                score = article.css('span.recipe-card__rating__value::text').get()

                to_pass = {
                    "title": title,
                    "link": link,
                    "image_link": image_link,
                    "duration":duration,
                    "score":score
                }
                # pour chaque article va dans la page associée
                yield response.follow(link, callback=self.parse_inner_page, cb_kwargs = to_pass)

            page_number += 1
            arg_next ={"page_number":page_number, "url":url}
            url2 = url + '/' + str(page_number) + '?rcp=0'

            yield scrapy.Request(url2, self.parse, cb_kwargs=arg_next)

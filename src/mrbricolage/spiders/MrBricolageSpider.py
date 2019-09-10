import scrapy
import re
import requests
import HTMLParser

class MrBricolageSpider(scrapy.Spider):
    name = 'MrBricolageBikeAccessories'
    start_urls = ['https://mr-bricolage.bg/bg/Instrumenti/Avto-i-veloaksesoari/Veloaksesoari/c/006008012/']

    API_URL = 'https://mr-bricolage.bg/store-pickup/986479/pointOfServices'

    def parse(self, response):
        #follow links to each item sub page
        for itemPage in response.xpath("//div[@class='image']/a/@href").extract():
            yield response.follow(itemPage, callback = self.parseItemPage)

        # follow pagination links
        for paginationNextPageLink in response.xpath("//li[@class='pagination-next']/a/@href").extract():
            if(paginationNextPageLink is not None):
                yield response.follow(paginationNextPageLink, self.parse)


    def parseItemPage(self, response):
        #Price selector will return a list with one item in it
        price = response.xpath("//*[contains(@class, 'js-product-price')]/@data-price-value").extract()

        if(len(price) > 0):
            price = str(float(price[0]))

        productCharacteristics = {}
        for characteristicsRow in response.xpath("//*[@class='product-classifications']//tbody//tr"):
            characteristicName = self.convertListItemToStr(characteristicsRow.xpath('td[1]//text()').extract())
            characteristicValue = self.convertListItemToStr(characteristicsRow.xpath('td[2]//text()').extract())

            productCharacteristics[characteristicName] = characteristicValue

        imgUrl = response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' owl-carousel-thumbs ')]//img/@src").extract()
        availabilityPerShop = self.getAvailibilityPerShop()

        yield {
            'title': self.convertListItemToStr(response.xpath("//*[contains(@class, 'js-product-name')]/text()").extract()),
            'price': price,
            'characteristics': productCharacteristics,
            'image_url': imgUrl,
            'shopAvailability': availabilityPerShop
        }

    def getAvailibilityPerShop(self):

        #Let's create the same AJAX call as from the web browser in order to fetch the availability per shop
        #Just copy'n'paste this POST body from the browser's request
        POSTBody = {
            'locationQuery': '',
            'cartPage': '0',
            'latitude': '42.6641056',
            'longitude': '23.3233149',
            'CSRFToken': '06ce5be0-f39f-490c-b56e-9fa2c3967fbc'
        }

        # Make the POST request
        response = requests.post(self.API_URL, data=POSTBody)

        result = []
        responseDataFields = {'displayName': 'shopLocation', 'line1': 'shopLocationAdditional', 'stockPickup': 'availablePieces'}

        for data in response.json()['data']:
            result.append(
                #It's needed to decode the HTML entities ex. &nbsp; in the stockPickup field
                { responseDataFields[responseFieldName]: self.unescapeHTMLEntities(data[responseFieldName]) for responseFieldName in responseDataFields }
            )

        return result

    def convertListItemToStr(self, list, removeSpecialChars = True):
        stringResult = "".join(list).strip()

        if removeSpecialChars:
            stringResult = re.sub(r"[\n\t.]", "", stringResult)

        return stringResult

    def unescapeHTMLEntities(self, text = ''):
        return HTMLParser.HTMLParser().unescape(text)

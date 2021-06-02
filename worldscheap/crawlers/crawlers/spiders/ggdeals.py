import scrapy
from crawlers.items import GameItem
class GameSpider(scrapy.Spider):

    name = 'ggdeals'
    #https://api.rawg.io/api/games/dragon-ball-z-kakarot/screenshots?key=b0dcfe4aac2f46209bf08e9cb1721387
    start_urls = ['https://gg.deals/game/industries-of-titan/',]
    # def start_requests(self):
    #     # urls = [
    #     #     'https://gg.deals/game/doraemon-story-of-seasons/',
            
    #     # ]
    #     self.url = 'https://gg.deals/game/doraemon-story-of-seasons/'
        
    #     yield scrapy.Request(url=self.url, callback=self.parse)


    def parse(self, response):
        i = GameItem()
        i['ggdeals_url'] = response.request.url
        i['name'] = response.xpath('//*[@class="game-price-anchor-link"]/h1/text()').get()

        i['developer_list'] = response.xpath("//*[@class='game-info-inner-heading' and contains(text(),'Developer')]/following-sibling::p/text()").get(default="---")
        i['release_date'] = response.xpath("//*[@class='game-info-inner-heading' and contains(text(),'Release date')]/following-sibling::p/text()").get(default="01 Jan 1900")
        i['description'] = response.xpath('//*[@id="about"]//div[contains(@class,"description-text")]').get()
        i['requirements'] = response.xpath('//*[@class="game-requirements-content"]').get()
        i['tag_list'] =response.xpath('//*[@id="game-info-tags"]//a/text()').getall()
        i['genre_list'] = response.xpath('//*[@id="game-info-genres"]/div/a/text()').getall()
        i['image_urls'] = response.xpath('//*[@class="game-info-image"]/img/@src')[0].getall() #header image
        i['image_urls'] += response.xpath('//*[@class="game-about-slider game-gallery-widget"]//a[contains(@href,".jpg")]/@href')[2].getall() #carousel images
        
        return i

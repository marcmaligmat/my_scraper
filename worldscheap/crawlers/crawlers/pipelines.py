from product.models_game import *
from scrapy.utils.misc import md5sum
from scrapy.pipelines.images import ImagesPipeline
import hashlib
from scrapy.utils.python import to_bytes
import datetime
from dateutil.parser import parse
import re

def clean_title(param):
    return param

def clean_critics_consensus(param):
    return ' '.join(param)

def clean_average_grade(param):
    param = param.strip().replace('/5', '')
    return param

def clean_poster(param):
    if param:
        param = param[0]['path']
    return param

def clean_amount_reviews(param):
    return param.strip()

def clean_approval_percentage(param):
    return param.strip().replace('%', '')

def clean_date(param):
    return parse(param,yearfirst=True).strftime('%Y-%m-%d')

def clean_name(param):
    return param.strip().replace('Buy ', '')

def get_slug(param):
    return param.strip().replace('https://gg.deals/game/', '').replace('/','')

def clean_developer(param):
    return param.split(", ")

def clean_html(param):
    return re.sub('(\").+\"',r'\g<1>"',str(param))

class StoreImgPipeline(ImagesPipeline):
    pass
        
class GamePipeline(ImagesPipeline):
    def process_item(self, item, spider):
        print('test')
        print(item)
        print('test')

        # title = clean_title(item['title'])
        header_image = clean_poster(item['images'])
        slug = get_slug(item['ggdeals_url'])
        name = clean_name(item['name'])
        developer_list = clean_developer(item['developer_list'])
        genre_m2m = self.get_or_create_m2m_data(item['genre_list'],Genre,'GENRE')
        developer_m2m = self.get_or_create_m2m_data(developer_list,Developer,'DEVELOPER')
        tag_m2m = self.get_or_create_m2m_data(item['tag_list'],Tag,'TAG')

        try:
            game = Game.objects.get(slug=slug)
            print("Game already exist")
            
        except Game.DoesNotExist:
            game = Game.objects.create(
                name=name,
                release_date=clean_date(item['release_date']),
                header_image=header_image,
                slug=slug,
                ggdeals_url=item['ggdeals_url'],
                requirements=clean_html(item['requirements']),
                description=clean_html(item['description']),
            )

            game.genre.set(genre_m2m)
            game.developer.set(developer_m2m)
            game.tag.set(tag_m2m)

        # game.pk
        for image in item['images'][1:]:
            
            if(image['status'] == 'downloaded'):
                GamePhoto.objects.create(
                    image=image['path'],
                    game=game
                )

        return item
    
    def get_or_create_m2m_data(self,data_list,model,model_name):
        returning_list = []
        for data in data_list:
            try:
                returning_list.append(model.objects.get(name=data))
                print(f"{data} {model_name} already exist")

            except model.DoesNotExist:
                returning_list.append( model.objects.create(
                    name=data,
                ))

        return returning_list
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from imagekit.models import ImageSpecField,ProcessedImageField
from imagekit.processors import Resize, ResizeToFill




def resizedImageSpec(length,width,processor,quality=100):
    return (
        ImageSpecField(source='image',
                        processors=[processor(length, width)],
                        format='JPEG',
                        options={'quality': quality}
        )
    )

    
def validate_image(image):
    file_size = image.file.size
    limit = 1000
    if file_size > limit * 1024:
        raise ValidationError("Max size of file is %s KB" % limit)


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Developer(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Game(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    release_date = models.DateField(blank=True)
    

    ggdeals_url = models.CharField('GG.DEALS URL',max_length=255, unique=True)
    slug = models.SlugField('Slug',max_length=255, unique=True)
    header_image = models.ImageField('Header Image', blank=True, null=True)

    publisher = models.ManyToManyField(Publisher)
    genre = models.ManyToManyField(Genre)
    tag = models.ManyToManyField(Tag)
    platform = models.ManyToManyField(Platform)
    developer = models.ManyToManyField(Developer)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # def save(self, *args, **kwargs):
    #     self.slug = slugify('buy '+self.name+ ' cheapest price')
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def image_home_small(self):
        return self.gamephotos.first().image_home_small.url
    
    def cheapest(self):
        # return self.gameProducts.last().price
        # return self.gameProducts.all()[:1]
        for cheapest in Game.objects.raw(
            f'''SELECT `price`,`id` 
            FROM product_product 
            WHERE game_id = {self.id} and price > 0 
            ORDER BY price ASC LIMIT 1 
            ''' ):
            return cheapest.price

    def image_home_medium(self):
        return self.gamephotos.first().image_home_medium.url

    def image_game_detail_carousel(self):
        return self.gamephotos.all()

    def get_products(self):
        return self.gameProducts.all().filter(price__gt=0).order_by('price')
    


class GamePhoto(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="gamephotos"
    )
    image = models.ImageField(  upload_to='game_photos/',
                                validators=[validate_image]) 
    image_home = resizedImageSpec(529,343,Resize)
    image_home_first = resizedImageSpec(457,343,Resize)
    image_home_small = resizedImageSpec(70,70,Resize)
    image_home_medium = resizedImageSpec(270,300,Resize)
    image_game_detail_carousel = resizedImageSpec(568,495,Resize)

    def __str__(self):
        return self.game.name


class GameComment(models.Model):
    game = models.ForeignKey(Game,
                                on_delete=models.CASCADE,
                                related_name='gamecomments')
    author = models.ForeignKey('auth.User', 
                                on_delete=models.CASCADE,
                                related_name='gamecommentAuthor')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_a_reply = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.author)
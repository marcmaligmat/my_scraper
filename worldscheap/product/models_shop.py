from django.db import models
from .models_game import resizedImageSpec,validate_image
from imagekit.models import ImageSpecField,ProcessedImageField
from imagekit.processors import Resize

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    def image_comparison_small(self):
        return self.shopPhotos.first().image_comparison_small.url

class Afflinks(models.Model):
    shop = models.ForeignKey('Shop', on_delete=models.DO_NOTHING)
    afflink = models.CharField(max_length=255)


class ShopPhoto(models.Model):
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="shopPhotos"
    )
    image = models.ImageField(upload_to='shop_photos/',validators=[validate_image]) 
    image_comparison_small = resizedImageSpec(146,68,Resize)

# class Review(models.Model):
#     url = models.CharField(max_length=255)
#     shop = models.ForeignKey('Shop',on_delete=models.DO_NOTHING)
#     rating = models.IntegerField(default=0)
#     ratingCount = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

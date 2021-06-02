from django.db import models
from .models_game import Game, Genre
from .models_shop import Shop



class Product(models.Model):
    url = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    edition = models.ForeignKey('Edition',on_delete=models.DO_NOTHING)
    region = models.ForeignKey('Region',on_delete=models.DO_NOTHING)
    game = models.ForeignKey('Game',related_name='gameProducts',on_delete=models.DO_NOTHING)
    shop = models.ForeignKey('Shop',related_name='shopProducts',on_delete=models.DO_NOTHING)
    other_id = models.IntegerField(default=0)
    other_id_2 = models.IntegerField(default=0)
    stock = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.url

    def get_cheapest(self,game_id):
        return Product.objects.filter(game_id=game_id).only("price")

class Edition(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

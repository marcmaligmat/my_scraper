from django.shortcuts import render,get_object_or_404
from product.models_game import Game, GamePhoto
from product.models import Product

photo = GamePhoto.objects.all().filter(game_id=1)[:1]



def home(request, *args, **kwargs):
    deals = Game.objects.all()
    return render(request, 'home.html',{
        "game": photo[0],
        "deals": deals
    })


def game_details(request,slug):
    game = get_object_or_404(Game,slug=slug)
    print(game.header_image)
    return render(request, 'game_detail.html',{
        "game": game,
        "products": game.get_products
    })
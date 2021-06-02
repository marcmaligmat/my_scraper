from django.contrib import admin

from accounts.models import Profile
from .models import Product, Edition, Region
from .models_game import Game,GameComment,GamePhoto,Genre,Platform,Publisher,Tag
from .models_shop import Shop, ShopPhoto
from .forms import GameAdminForm, ShopAdminForm
from django.template.loader import get_template
from django.utils.translation import gettext as _

class ShowPhotoInline(admin.TabularInline):
    model = GamePhoto
    fields = ("gamephoto_thumbnail",)
    readonly_fields = ("gamephoto_thumbnail",)
    verbose_name_plural = "PHOTOS"
    max_num = 0

    def gamephoto_thumbnail(self, instance):
        """A (pseudo)field that returns an image thumbnail for a show photo."""
        tpl = get_template("show_thumb.html")
        return tpl.render({"image": instance.image})
    gamephoto_thumbnail.short_description = _("Thumbnail")


class ShopPhotoInline(admin.TabularInline):
    model = ShopPhoto
    fields = ("gamephoto_thumbnail",)
    readonly_fields = ("gamephoto_thumbnail",)
    verbose_name_plural = "PHOTOS"
    max_num = 0

    def gamephoto_thumbnail(self, instance):
        """A (pseudo)field that returns an image thumbnail for a show photo."""
        tpl = get_template("show_thumb.html")
        return tpl.render({"image": instance.image})

    gamephoto_thumbnail.short_description = _("Thumbnail")

@admin.register(Game)
class ShowAdmin(admin.ModelAdmin):
    form = GameAdminForm
    inlines = [ShowPhotoInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_photos(form.instance)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    form = ShopAdminForm
    inlines = [ShopPhotoInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_photos(form.instance)


#Product related classes
admin.site.register(Product)
admin.site.register(Edition)
admin.site.register(Region)



#game related class

admin.site.register(Genre)
admin.site.register(Publisher)
admin.site.register(Tag)
admin.site.register(Platform)
admin.site.register(GameComment)

admin.site.register(Profile)
admin.site.register(GamePhoto)
admin.site.site_header = "WORLDS CHEAP"
admin.site.site_title = "WORLDS CHEAP Admin Portal"
admin.site.index_title = "WORLDS CHEAP ADMIN"
from django import forms
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext as _

from .models_game import Game, GamePhoto
from .models_shop import Shop, ShopPhoto
   
class GameAdminForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = (
            "name",
            "description",
            "summary",
            "requirements",
            "release_date",
            "genre",
            "tag",
            "platform",
            "header_image",
            "slug"

        )

    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        label=_("Add photos"),
        required=False,
    )

    def clean_photos(self):
        """Make sure only images can be uploaded."""
        for upload in self.files.getlist("images"):
            validate_image_file_extension(upload)

    def save_photos(self, game):
        """Process each uploaded image."""
        for upload in self.files.getlist("images"):
            image = GamePhoto(game=game, image=upload)
            image.save()

class ShopAdminForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = (
            "name",
        )

    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        label=_("Add photos"),
        required=False,
    )

    def clean_photos(self):
        """Make sure only images can be uploaded."""
        for upload in self.files.getlist("images"):
            validate_image_file_extension(upload)

    def save_photos(self, shop):
        """Process each uploaded image."""
        for upload in self.files.getlist("images"):
            image = ShopPhoto(shop=shop, image=upload)
            image.save()
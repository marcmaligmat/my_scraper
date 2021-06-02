from rest_framework import serializers
from product.models_game import GameComment


class GameCommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    gamename = serializers.CharField(source="game.name", read_only=True)
    gameslug = serializers.CharField(source="game.slug", read_only=True)
    class Meta:
        model = GameComment
        fields = ('id', 'author', 'game','gamename','gameslug','body')


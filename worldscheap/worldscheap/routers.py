from api.viewsets import GameCommentViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('gamecomments', GameCommentViewSet)
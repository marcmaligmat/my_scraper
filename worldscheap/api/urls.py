from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from api.views import GameCommentViewSet, UserViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter



gamecomment_list = GameCommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
gamecomment_detail = GameCommentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
# snippet_highlight = GameCommentViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'gamecomments', views.GameCommentViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
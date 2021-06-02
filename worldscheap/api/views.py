from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from api.permissions import IsOwnerOrReadOnly
from .serializers import GameCommentSerializer
from product.models_game import GameComment
from django.contrib.auth.models import User
# Create your views here.


class GameCommentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = GameComment.objects.all()
    serializer_class = GameCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    filter_fields = ["game"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
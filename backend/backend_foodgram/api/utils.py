from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from .serializers import FollowRecipesSerializer


def add_delete(request, model, obj_id):
    user = request.user
    if request.method == 'DELETE':
        obj = model.objects.filter(
            user=user,
            recipe__id=obj_id
        )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            status=status.HTTP_400_BAD_REQUEST)
    if model.objects.filter(
        user=user,
        recipe__id=obj_id
    ).exists():
        return Response(
            status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(
        Recipe,
        id=obj_id
    )
    model.objects.create(
        user=user,
        recipe=recipe
    )
    serializer = FollowRecipesSerializer(recipe)
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from recipes.models import (Favorite, Ingredient, IngredientQuantity, Recipe,
                            ShoppingCart, Tag)
from users.models import CustomUser, Follow
from .filters import IngredientFilter, UserRecipeFilter
from .paginator import PageNumberPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, 
                          FollowSerializer, FollowListSerializer,
                          IngredientSerializer,
                          RecipeListSerializer, RecipeWriteSerializer,
                          ShoppingCartSerializer, TagSerializer)


class FollowApiView(APIView):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post', ],)
    def post(self, request, id):
        data = {'user': request.user.id, 'following': id}
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(CustomUser, id=id)
        follow = get_object_or_404(
            Follow, user=user, following=following
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = CustomUser.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(
            page, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_class = UserRecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeWriteSerializer

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='favorite',
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': pk}
            serializer = FavoriteSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            favorite = get_object_or_404(
                Favorite, user=user, recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None
    
    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': pk}
            serializer = ShoppingCartSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            shopping_cart = get_object_or_404(
                ShoppingCart, user=user, recipe=recipe
            )
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None
    
    @action(
        detail=False,
        url_path='download_shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        cart_list = IngredientQuantity.objects.filter(
            recipe__shopping_carts__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(sum_amount=Sum('amount'))
        list_cart = []
        for step, ingredient in enumerate(cart_list, start=1):
            name = ingredient["ingredient__name"]
            amount = ingredient["sum_amount"]
            unit = ingredient["ingredient__measurement_unit"]
            list_cart.append(
                f'{step}. '
                f'{name} '
                f'{amount} '
                f'{unit}\n',
            )
        response = HttpResponse(
            list_cart,
            content_type='text/plain'
        )
        response['Content-Disposition'] = (
            'attachment; '
            'filename="shopping_list.txt"'
        )
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_class = IngredientFilter
    permission_classes = (IsAdminOrReadOnly,)

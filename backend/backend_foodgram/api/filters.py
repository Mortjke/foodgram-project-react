from django.contrib import admin
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class UserRecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name="slug",
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            queryset = queryset.filter(
                favourites__user=self.request.user
            )
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            queryset = queryset.filter(
                cart_shoppings__user=self.request.user
            )
        return queryset


class IngredientFilterAdmin(admin.SimpleListFilter):

    title = 'Ингредиенты'
    parameter_name = 'ингредиенты_категории'

    def lookups(self, request, model_admin):
        pattern = 'абвгдеёжзийклмнопрстуфхцчшщэюя'
        return [(i, i) for i in pattern]

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(name__startswith=self.value())
        return

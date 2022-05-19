from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Ingredient, IngredientQuantity, Recipe, Tag

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(IngredientQuantity)

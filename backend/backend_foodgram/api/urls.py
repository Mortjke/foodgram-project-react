from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                    FollowApiView, FollowListAPIView)

router = DefaultRouter()


router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:id>/subscribe/', FollowApiView.as_view(),
         name='subscribe'),
    path('users/subscriptions/', FollowListAPIView.as_view(),
         name='subscription'),
]

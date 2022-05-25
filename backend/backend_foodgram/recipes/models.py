from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет тега'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг тега'
    )

    class Meta:
        verbose_name = 'Tег'
        verbose_name_plural = 'Tеги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы изменения'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=False,
        verbose_name='Изображение рецепта'
    )
    text = models.TextField(verbose_name='Текст рецепта')
    ingredients = models.ManyToManyField(
        Ingredient, 
        through='IngredientQuantity',
        verbose_name='Ингридиенты рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, message='Время приготовления должно быть больше 0!'
            )
        ],
        verbose_name='Время приготовления в минутах'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    ingredients = models.ForeignKey(
        Ingredient, 
        on_delete=models.CASCADE,
        verbose_name='Ингридиенты рецепта'
    )
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, 'Минимальное кол-во ингридиента равно 1'
            )
        ],
        verbose_name='Количество ингридиентов'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredients', 'recipe'],
                name='Ингридиенты можно использовать только 1 раз!'
            )
        ]
        verbose_name = 'Ингридиент рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'
   
    def __str__(self):
        return f'{self.recipe} {self.ingredients}'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='favorites',
        verbose_name='Оценивший пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='Этот рецепт уже в избранном!'
        )
        ]
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'{self.recipe}{self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь, добавивший ингр. в корзину'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт в корзине пользователя'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='Рецепт уже находится в корзине!'
        )
        ]
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'

    def __str__(self):
        return f'{self.recipe}{self.user}'

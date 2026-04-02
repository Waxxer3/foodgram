from django.contrib import admin
from django.db.models import Count

from .models import (
    Recipe,
    Tag,
    Ingredient,
    IngredientInRecipe,
    Favorite,
    ShoppingCart
)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1
    autocomplete_fields = ('ingredient',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    list_editable = ('color',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'get_favorites_count',
        'pub_date',
    )
    search_fields = ('name', 'author__username', 'author__email')
    list_filter = ('tags', 'author')
    inlines = (IngredientInRecipeInline,)

    @admin.display(description='В избранном', ordering='fav_count')
    def get_favorites_count(self, obj):
        return getattr(obj, 'fav_count', 0)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(fav_count=Count('favorites'))


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__email', 'recipe__name')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__email', 'recipe__name')

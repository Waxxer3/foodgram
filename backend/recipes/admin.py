from django.contrib import admin
from django.db.models import Count
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import (
    Recipe,
    Tag,
    Ingredient,
    IngredientInRecipe,
    Favorite,
    ShoppingCart
)


class IngredientInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        count = 0
        for form in self.forms:
            if (not form.cleaned_data.get('DELETE')
                    and form.cleaned_data.get('ingredient')):
                count += 1
        if count < 1:
            raise ValidationError('Добавьте хотя бы один ингредиент!')


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    formset = IngredientInlineFormset
    min_num = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name')
    search_fields = ('name',)


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


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__email', 'recipe__name')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__email', 'recipe__name')

from django_filters.rest_framework import FilterSet, filters

from .models import Recipe


class RecipeFilter(FilterSet):
    """
    Фильтр для рецептов.
    Позволяет фильтровать по тегам, автору, наличию в избранном и корзине.
    """
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='filter_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_shopping')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_favorited(self, queryset, name, value):
        """Фильтрация рецептов, добавленных в избранное."""
        user = self.request.user
        if user.is_authenticated and value:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_shopping(self, queryset, name, value):
        """Фильтрация рецептов, добавленных в список покупок."""
        user = self.request.user
        if user.is_authenticated and value:
            return queryset.filter(shopping_cart__user=user)
        return queryset

import django_filters

from .models import Recipe


class RecipeFilter(django_filters.FilterSet):
    """
    Фильтр для рецептов.
    Позволяет фильтровать по тегам, автору, наличию в избранном и корзине.
    """
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = django_filters.NumberFilter(field_name='author__id')
    is_favorited = django_filters.NumberFilter(method='filter_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(method='filter_shopping')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_favorited(self, queryset, name, value):
        """Фильтрация рецептов, добавленных в избранное."""
        user = self.request.user
        if user.is_authenticated and value == 1:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_shopping(self, queryset, name, value):
        """Фильтрация рецептов, добавленных в список покупок."""
        user = self.request.user
        if user.is_authenticated and value == 1:
            return queryset.filter(shopping_cart__user=user)
        return queryset

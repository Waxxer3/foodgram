from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с пользователем.
    Добавляет проверку подписки текущего пользователя на автора.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Проверка подписки текущего пользователя на этого автора."""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return obj.subscribers.filter(user=request.user).exists()


class SubscribeSerializer(UserSerializer):
    """
    Сериализатор для отображения подписок пользователя.
    Выводит автора, его рецепты и их общее количество.
    """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='recipes.count')

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )
        read_only_fields = fields

    def get_recipes(self, obj):
        """Получение списка рецептов автора с учетом лимита."""
        from recipes.serializers import ShortRecipeSerializer
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        queryset = obj.recipes.all()

        if limit:
            try:
                queryset = queryset[:int(limit)]
            except (ValueError, TypeError):
                pass

        return ShortRecipeSerializer(
            queryset,
            many=True,
            context={'request': request}
        ).data

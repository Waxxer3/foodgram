from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.serializers import ShortRecipeSerializer
from .models import User, Subscription


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с пользователем.
    Добавляет проверку подписки текущего пользователя на автора.
    """
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
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
            'last_name', 'is_subscribed', 'recipes', 'recipes_count',
            'avatar',
        )
        read_only_fields = fields

    def get_recipes(self, obj):
        """Получение списка рецептов автора с учетом лимита."""
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


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/удаления подписки."""

    class Meta:
        model = Subscription
        fields = ('user', 'author')

    def validate(self, data):
        user = data['user']
        author = data['author']
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        if Subscription.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора'
            )
        return data

    def to_representation(self, instance):
        return SubscribeSerializer(
            instance.author,
            context=self.context
        ).data

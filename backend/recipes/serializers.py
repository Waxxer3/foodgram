from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Subscription


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с ингредиентами."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с тегами."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientInRecipeReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientInRecipeWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения полной информации о рецепте."""
    image = Base64ImageField()
    author = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientInRecipeReadSerializer(
        source='recipe_ingredients',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'image',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_author(self, obj):
        request = self.context.get('request')
        user = obj.author
        is_subscribed = False

        if request and request.user.is_authenticated:
            is_subscribed = Subscription.objects.filter(
                user=request.user,
                author=user
            ).exists()

        avatar_url = None
        if user.avatar:
            try:
                if request:
                    avatar_url = request.build_absolute_uri(
                        user.avatar.url
                    )
                else:
                    avatar_url = user.avatar.url
            except (ValueError, AttributeError):
                avatar_url = None

        return {
            'email': user.email,
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_subscribed': is_subscribed,
            'avatar': avatar_url
        }

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientInRecipeWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'text',
            'ingredients',
            'tags',
            'cooking_time'
        )

    def validate(self, data):
        """Проверка уникальности ингредиентов и тегов."""
        ingredients = data.get('ingredients')
        tags = data.get('tags')

        if not ingredients:
            raise serializers.ValidationError('Нужен хотя бы один ингредиент')
        if not tags:
            raise serializers.ValidationError('Нужен хотя бы один тег')

        ingredient_ids = [item['id'] for item in ingredients]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться'
            )

        if len(tags) != len(set(tags)):
            raise serializers.ValidationError('Теги не должны повторяться')

        return data

    def create_ingredients(self, recipe, ingredients_data):
        for ingredient_data in ingredients_data:
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_data['id'],
                amount=ingredient_data['amount']
            )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        request = self.context.get('request')
        user = request.user
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        ingredients_data = validated_data.pop('ingredients', None)

        if tags is not None:
            instance.tags.set(tags)
        if ingredients_data is not None:
            instance.recipe_ingredients.all().delete()
            self.create_ingredients(instance, ingredients_data)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Возвращает данные через RecipeReadSerializer после записи."""
        return {'id': instance.id, 'status': 'success'}


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор рецепта для избранного и корзины."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

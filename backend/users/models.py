from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """Кастомная модель пользователя. Вход по email вместо username."""
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    username = models.CharField('Никнейм', max_length=150, unique=True)
    avatar = models.ImageField(
        'Аватар',
        upload_to='users/images/',
        null=True,
        blank=True
    )
    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',
        blank=True,
        verbose_name='Группы'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users_permissions',
        blank=True,
        verbose_name='Права пользователя'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'{self.email} ({self.username})'


class Subscription(models.Model):
    """Модель подписок на авторов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'author')

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Нельзя подписаться на самого себя')

    def __str__(self):
        return f'{self.user} подписан на {self.author}'

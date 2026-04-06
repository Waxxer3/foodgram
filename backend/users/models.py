from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import EMAIL_MAX_LENGTH, USER_FIELD_MAX_LENGTH


class User(AbstractUser):
    """Кастомная модель пользователя. Вход по email вместо username."""
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )
    first_name = models.CharField('Имя', max_length=USER_FIELD_MAX_LENGTH)
    last_name = models.CharField('Фамилия', max_length=USER_FIELD_MAX_LENGTH)
    username = models.CharField(
        'Никнейм',
        max_length=USER_FIELD_MAX_LENGTH,
        unique=True
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to='users/images/',
        null=True,
        blank=True
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
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='no_self_subscription'
            )
        ]

    def __str__(self): 
        return f'{self.user} подписан на {self.author}'

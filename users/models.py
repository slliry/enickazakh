from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Менеджер пользователей с поддержкой email вместо username."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Создает и возвращает пользователя с email и паролем."""
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и возвращает суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.ADMIN)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Пользовательская модель с ролями и аутентификацией по email."""
    
    # Роли пользователей
    USER = 'user'
    ADMIN = 'admin'
    UNIVERSITY = 'university'
    
    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (UNIVERSITY, 'ВУЗ'),
    ]
    
    email = models.EmailField(_('Email'), unique=True)
    university_name = models.CharField(_('Наименование ВУЗа'), max_length=255, blank=True)
    first_name = models.CharField(_('Имя'), max_length=150, blank=True)
    last_name = models.CharField(_('Фамилия'), max_length=150, blank=True)
    role = models.CharField(_('Роль'), max_length=20, choices=ROLE_CHOICES, default=USER)
    is_staff = models.BooleanField(
        _('Статус персонала'),
        default=False,
        help_text=_('Определяет, может ли пользователь входить в админ-панель.'),
    )
    is_active = models.BooleanField(
        _('Активен'),
        default=True,
        help_text=_(
            'Определяет, следует ли считать этого пользователя активным. '
            'Снимите этот флажок вместо удаления учетных записей.'
        ),
    )
    date_joined = models.DateTimeField(_('Дата регистрации'), default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
    
    def get_full_name(self):
        """Возвращает полное имя пользователя или название ВУЗа."""
        if self.role == self.UNIVERSITY:
            return self.university_name
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.email
    
    def get_short_name(self):
        """Возвращает короткое имя пользователя или название ВУЗа."""
        if self.role == self.UNIVERSITY:
            return self.university_name
        return self.first_name if self.first_name else self.email
    
    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором."""
        return self.role == self.ADMIN
    
    @property
    def is_university(self):
        """Проверяет, является ли пользователь ВУЗом."""
        return self.role == self.UNIVERSITY


class PasswordResetToken(models.Model):
    """Модель для хранения токенов сброса пароля."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Token for {self.user.email}"

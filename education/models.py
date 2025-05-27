from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Program(models.Model):
    """Модель образовательной программы."""
    
    name = models.CharField(_('Название'), max_length=255)
    description = models.TextField(_('Описание'))
    duration = models.PositiveIntegerField(_('Продолжительность (месяцев)'))
    start_date = models.DateField(_('Дата начала'))
    end_date = models.DateField(_('Дата окончания'))
    is_active = models.BooleanField(_('Активна'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    class Meta:
        verbose_name = _('образовательная программа')
        verbose_name_plural = _('образовательные программы')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Accreditation(models.Model):
    """Модель аккредитации образовательной программы."""
    
    program = models.ForeignKey(
        Program, 
        on_delete=models.CASCADE, 
        related_name='accreditations',
        verbose_name=_('Программа')
    )
    name = models.CharField(_('Название аккредитации'), max_length=255)
    organization = models.CharField(_('Аккредитующая организация'), max_length=255)
    date_received = models.DateField(_('Дата получения'))
    expiration_date = models.DateField(_('Дата истечения'))
    certificate_number = models.CharField(_('Номер сертификата'), max_length=100)
    description = models.TextField(_('Описание'), blank=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    class Meta:
        verbose_name = _('аккредитация')
        verbose_name_plural = _('аккредитации')
        ordering = ['-date_received']
    
    def __str__(self):
        return f"{self.name} - {self.program.name}"


class Publication(models.Model):
    """Модель публикации (научной статьи, книги и т.д.)."""
    
    title = models.CharField(_('Заголовок'), max_length=255)
    authors = models.ManyToManyField(
        User,
        related_name='publications',
        verbose_name=_('Авторы')
    )
    publication_date = models.DateField(_('Дата публикации'))
    journal_name = models.CharField(_('Название журнала/издания'), max_length=255, blank=True)
    doi = models.CharField(_('DOI'), max_length=100, blank=True)
    url = models.URLField(_('URL'), blank=True)
    abstract = models.TextField(_('Аннотация'), blank=True)
    keywords = models.CharField(_('Ключевые слова'), max_length=255, blank=True)
    file = models.FileField(_('Файл публикации'), upload_to='publications/', blank=True, null=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    class Meta:
        verbose_name = _('публикация')
        verbose_name_plural = _('публикации')
        ordering = ['-publication_date']
    
    def __str__(self):
        return self.title


class MobilityProgram(models.Model):
    """Модель программы мобильности (обмена)."""
    
    name = models.CharField(_('Название'), max_length=255)
    description = models.TextField(_('Описание'))
    host_institution = models.CharField(_('Принимающее учреждение'), max_length=255)
    country = models.CharField(_('Страна'), max_length=100)
    city = models.CharField(_('Город'), max_length=100)
    start_date = models.DateField(_('Дата начала'))
    end_date = models.DateField(_('Дата окончания'))
    application_deadline = models.DateField(_('Крайний срок подачи заявок'))
    requirements = models.TextField(_('Требования'), blank=True)
    benefits = models.TextField(_('Преимущества'), blank=True)
    contact_email = models.EmailField(_('Контактный email'), blank=True)
    website = models.URLField(_('Веб-сайт'), blank=True)
    is_active = models.BooleanField(_('Активна'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    class Meta:
        verbose_name = _('программа мобильности')
        verbose_name_plural = _('программы мобильности')
        ordering = ['-application_deadline']
    
    def __str__(self):
        return f"{self.name} - {self.host_institution} ({self.country})"

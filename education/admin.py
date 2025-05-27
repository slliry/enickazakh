from django.contrib import admin
from .models import Program, Accreditation, Publication, MobilityProgram


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """Административная панель для образовательных программ."""
    
    list_display = ('name', 'duration', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    date_hierarchy = 'start_date'


@admin.register(Accreditation)
class AccreditationAdmin(admin.ModelAdmin):
    """Административная панель для аккредитаций."""
    
    list_display = ('name', 'program', 'organization', 'date_received', 'expiration_date')
    list_filter = ('organization', 'date_received', 'expiration_date')
    search_fields = ('name', 'program__name', 'organization', 'certificate_number')
    date_hierarchy = 'date_received'
    autocomplete_fields = ['program']


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    """Административная панель для публикаций."""
    
    list_display = ('title', 'publication_date', 'journal_name')
    list_filter = ('publication_date',)
    search_fields = ('title', 'abstract', 'keywords', 'journal_name', 'authors__email')
    date_hierarchy = 'publication_date'
    filter_horizontal = ('authors',)


@admin.register(MobilityProgram)
class MobilityProgramAdmin(admin.ModelAdmin):
    """Административная панель для программ мобильности."""
    
    list_display = ('name', 'host_institution', 'country', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'country', 'application_deadline')
    search_fields = ('name', 'description', 'host_institution', 'country', 'city')
    date_hierarchy = 'application_deadline'

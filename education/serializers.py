from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Program, Accreditation, Publication, MobilityProgram

User = get_user_model()


class UserBriefSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для модели пользователя."""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class ProgramSerializer(serializers.ModelSerializer):
    """Сериализатор для модели образовательной программы."""
    
    class Meta:
        model = Program
        fields = '__all__'


class AccreditationSerializer(serializers.ModelSerializer):
    """Сериализатор для модели аккредитации."""
    
    program_name = serializers.ReadOnlyField(source='program.name')
    
    class Meta:
        model = Accreditation
        fields = '__all__'


class PublicationSerializer(serializers.ModelSerializer):
    """Сериализатор для модели публикации."""
    
    authors = UserBriefSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='authors'
    )
    
    class Meta:
        model = Publication
        fields = ['id', 'title', 'authors', 'author_ids', 'publication_date', 'journal_name', 
                  'doi', 'url', 'abstract', 'keywords', 'file', 'created_at', 'updated_at']


class MobilityProgramSerializer(serializers.ModelSerializer):
    """Сериализатор для модели программы мобильности."""
    
    class Meta:
        model = MobilityProgram
        fields = '__all__'


# Расширенные сериализаторы для детального представления

class ProgramDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для модели образовательной программы."""
    
    accreditations = AccreditationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Program
        fields = '__all__'


class AccreditationDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для модели аккредитации."""
    
    program = ProgramSerializer(read_only=True)
    
    class Meta:
        model = Accreditation
        fields = '__all__' 
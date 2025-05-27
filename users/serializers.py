from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from .models import PasswordResetToken
import uuid

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'university_name', 'first_name', 'last_name', 'role', 'date_joined']
        read_only_fields = ['date_joined', 'role']


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""
    
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": _("Пароли не совпадают.")})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UniversityCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя типа ВУЗ."""
    
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['email', 'university_name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": _("Пароли не совпадают.")})
        
        if not attrs.get('university_name'):
            raise serializers.ValidationError({"university_name": _("Наименование ВУЗа обязательно.")})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data['role'] = User.UNIVERSITY
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Сериализатор для аутентификации пользователя."""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                msg = _('Невозможно войти с предоставленными учетными данными.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Должны быть указаны "email" и "password".')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    """Сериализатор для запроса сброса пароля."""
    
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("Пользователь с таким email не найден."))
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Сериализатор для подтверждения сброса пароля."""
    
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": _("Пароли не совпадают.")})
        
        try:
            token_obj = PasswordResetToken.objects.get(token=attrs['token'], is_used=False)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({"token": _("Недействительный или использованный токен.")})
        
        attrs['token_obj'] = token_obj
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""
    
    old_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    new_password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Текущий пароль неверен."))
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": _("Пароли не совпадают.")})
        return attrs 
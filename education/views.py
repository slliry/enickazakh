from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Program, Accreditation, Publication, MobilityProgram
from .serializers import (
    ProgramSerializer, ProgramDetailSerializer,
    AccreditationSerializer, AccreditationDetailSerializer,
    PublicationSerializer, MobilityProgramSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет администраторам выполнять любые действия,
    а обычным пользователям - только чтение.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_admin


class ProgramViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с образовательными программами."""
    
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProgramDetailSerializer
        return self.serializer_class


class AccreditationViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с аккредитациями."""
    
    queryset = Accreditation.objects.all()
    serializer_class = AccreditationSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AccreditationDetailSerializer
        return self.serializer_class
    
    @action(detail=False, methods=['get'])
    def by_program(self, request):
        """Получение аккредитаций по ID программы."""
        program_id = request.query_params.get('program_id')
        if program_id:
            accreditations = Accreditation.objects.filter(program_id=program_id)
            serializer = self.get_serializer(accreditations, many=True)
            return Response(serializer.data)
        return Response({"detail": "Необходимо указать program_id."}, status=400)


class PublicationViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с публикациями."""
    
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def my_publications(self, request):
        """Получение публикаций текущего пользователя."""
        if request.user.is_authenticated:
            publications = Publication.objects.filter(authors=request.user)
            serializer = self.get_serializer(publications, many=True)
            return Response(serializer.data)
        return Response({"detail": "Необходима аутентификация."}, status=401)


class MobilityProgramViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с программами мобильности."""
    
    queryset = MobilityProgram.objects.all()
    serializer_class = MobilityProgramSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Получение только активных программ мобильности."""
        active_programs = MobilityProgram.objects.filter(is_active=True)
        serializer = self.get_serializer(active_programs, many=True)
        return Response(serializer.data)

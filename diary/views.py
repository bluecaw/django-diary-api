
from rest_framework import viewsets
from .models import Diary
from .serializers import DiarySerializer


class DiaryViewSet(viewsets.ModelViewSet):
    serializer_class = DiarySerializer

    def get_queryset(self):
        return Diary.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

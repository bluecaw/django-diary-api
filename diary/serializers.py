
from rest_framework import serializers
from .models import Diary


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = [
            "id",
            "date",
            "title",
            "content",
            "owner",
            "good",
            "bad",
            "cool",
            "ai_comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]

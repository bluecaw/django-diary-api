from django.conf import settings
from django.db import models


class Diary(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200)
    content = models.TextField()

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diaries",
    )

    good = models.BooleanField(default=False)
    bad = models.BooleanField(default=False)
    cool = models.BooleanField(default=False)

    ai_comment = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

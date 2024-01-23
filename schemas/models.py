from django.conf import settings
from django.db import models


class DataType(models.Model):
    name = models.CharField(max_length=60, unique=True)
    allow_range = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Schema(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schemas"
    )

    def __str__(self) -> str:
        return self.title


class Column(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    min_value = models.IntegerField(null=True, blank=True)
    max_value = models.IntegerField(null=True, blank=True)

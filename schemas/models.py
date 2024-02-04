from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Schema(models.Model):
    COMMA = ","
    SEMICOLON = ";"
    TAB = "\t"

    DOUBLE_QUOTE = '"'
    SINGLE_QUOTE = '"'

    SEPARATOR_CHOICES = [
        (COMMA, "Comma(,)"),
        (SEMICOLON, "Semicolon(;)"),
        (TAB, "Tab(\t)")
    ]

    STRING_CHARACTER_CHOICES = [
        (DOUBLE_QUOTE, 'Double Quotes(")'),
        (SINGLE_QUOTE, "Single Quotes(')")
    ]

    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schemas"
    )
    column_separator = models.CharField(max_length=1,  choices=SEPARATOR_CHOICES)
    string_character = models.CharField(max_length=1, choices=STRING_CHARACTER_CHOICES)

    def __str__(self) -> str:
        return self.title


class Column(models.Model):
    DATA_TYPE_CHOICES = [
        ("Integer", "Integer"),
        ("Full name", "Full name"),
        ("Job", "Job"),
        ("Phone number", "Phone number"),
        ("Company", "Company"),
        ("Text", "Text"),
        ("Date", "Date"),
        ("Address", "Address")
    ]

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name="columns",)
    name = models.CharField(max_length=64)
    data_type = models.CharField(max_length=64, choices=DATA_TYPE_CHOICES)
    min_value = models.IntegerField(null=True, blank=True)
    max_value = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ("schema", "order")

    def __str__(self) -> str:
        return f"Schema id {self.schema} {self.name}"


class DataSet(models.Model):
    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name="datasets"
    )
    created_at = models.DateTimeField(auto_now=True)
    number_of_rows = models.IntegerField(validators=[MinValueValidator(1)])
    file = models.CharField(max_length=255, blank=True)
    is_ready = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.schema} {self.created_at}"

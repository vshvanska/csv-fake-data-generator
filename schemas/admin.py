from django.contrib import admin

from schemas.models import DataType, Schema, Column


@admin.register(Schema)
class SchemasAdmin(admin.ModelAdmin):
    list_display = ("title", "user",)
    list_filter = ("user",)


admin.site.register(DataType)
admin.site.register(Column)

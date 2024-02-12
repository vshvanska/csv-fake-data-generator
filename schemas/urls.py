from django.urls import path
from .views import create_schema, SchemaList, SchemaDelete, SchemaDetail, download_file

urlpatterns = [
    path("schema/create/", create_schema, name="create_schema"),
    path("", SchemaList.as_view(), name="schema-list"),
    path("schema/<int:pk>/", SchemaDetail.as_view(), name="schema-detail"),
    path("schema/delete/<int:pk>/", SchemaDelete.as_view(), name="schema-delete"),
    path("dataset/<int:pk>/download/", download_file, name="download-file"),
]

app_name = "schemas"

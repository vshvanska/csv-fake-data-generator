from django.urls import path
from .views import create_schema, SchemaList, SchemaDelete, SchemaDetail

urlpatterns = [
    path('schema/create/',  create_schema, name='create_schema'),
    path("", SchemaList.as_view(), name="schema-list"),
    path("schema/<int:pk>/", SchemaDetail.as_view(), name="schema-detail"),
    path("schema/delete/<int:pk>/", SchemaDelete.as_view(), name="schema-delete")

]

app_name = "schemas"

from django.urls import path
from .views import create_schema, SchemaList, SchemaDelete

urlpatterns = [
    path('schema/create/',  create_schema, name='create_schema'),
    path("", SchemaList.as_view(), name="schema-list"),
    path("schema/delete/<int:pk>/", SchemaDelete.as_view(), name="schema-delete")

]

app_name = "schemas"

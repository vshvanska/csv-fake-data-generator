from django.urls import path
from .views import create_schema

urlpatterns = [
    path('create/',  create_schema, name='create_schema'),
    # Додайте інші URL-адреси за необхідності
]

app_name = "schemas"

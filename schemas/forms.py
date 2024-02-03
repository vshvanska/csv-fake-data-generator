from django import forms
from .models import Schema, Column


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ['title', 'column_separator', 'string_character', "number_of_rows"]


ColumnFormset = forms.modelformset_factory(
    Column,
    fields='__all__',
    extra=1,
    exclude=['schema'],)
    
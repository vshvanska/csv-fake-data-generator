from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import SchemaForm, ColumnFormset
from .models import Schema, Column


def create_schema(request):
    schema_form = SchemaForm(request.GET or None)
    formset = ColumnFormset(queryset=Column.objects.none())
    if request.method == 'POST':
        schema_form = SchemaForm(request.POST)
        formset = ColumnFormset(request.POST)
        if schema_form.is_valid() and formset.is_valid():
            schema = schema_form.save(commit=False)
            schema.user = get_user_model().objects.get(pk=request.user.pk)
            schema = schema_form.save()

            for form in formset:
                column = form.save(commit=False)
                column.schema = schema
                column.save()
                print(column.schema)
            return redirect('schemas:schema-list')
    return render(request, "schemas/schema_create.html", {'form': schema_form,
                                                          'formset': formset})


class SchemaList(generic.ListView):
    model = Schema
    paginate_by = 5
    queryset = Schema.objects.select_related("user")


class SchemaDelete(generic.DeleteView):
    model = Schema
    success_url = reverse_lazy("schemas:schema-list")


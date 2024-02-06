import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import SchemaForm, ColumnFormset
from .models import Schema, Column, DataSet
from .task import create_fake_data


def create_schema(request):
    schema_form = SchemaForm(request.GET or None)
    formset = ColumnFormset(queryset=Column.objects.none())
    if request.method == "POST":
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
            return redirect("schemas:schema-list")
    return render(
        request, "schemas/schema_create.html", {"form": schema_form, "formset": formset}
    )


class SchemaList(LoginRequiredMixin, generic.ListView):
    model = Schema
    paginate_by = 5
    queryset = Schema.objects.select_related("user")


class SchemaDetail(generic.DetailView):
    model = Schema

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("datasets", "columns")

    def post(self, request, *args, **kwargs):
        schema_id = kwargs["pk"]
        schema = self.get_object()

        number_of_rows = request.POST.get("number_of_rows")

        if number_of_rows:
            dataset = schema.datasets.create(
                schema=schema_id, number_of_rows=number_of_rows
            )
            dataset.save()
            create_fake_data.delay(dataset.id, schema_id)

        return HttpResponseRedirect(
            reverse("schemas:schema-detail", kwargs={"pk": schema_id})
        )


class SchemaDelete(LoginRequiredMixin, generic.DeleteView):
    model = Schema
    success_url = reverse_lazy("schemas:schema-list")


def download_file(request, pk):
    dataset = get_object_or_404(DataSet, pk=pk)
    file_path = dataset.file.url[1:]
    file_absolute_path = os.path.join(settings.MEDIA_ROOT, file_path)
    with open(file_absolute_path, "rb") as file:
        response = HttpResponse(file.read(), content_type="application/octet-stream")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{os.path.basename(file_absolute_path)}"'
        return response

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    fields = ("first_name", "last_name", "email")
    template_name = "schemas/user_form.html"
    success_url = reverse_lazy("schemas:schema-list")

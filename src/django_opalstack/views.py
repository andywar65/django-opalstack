from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import ListView

from .models import Token


class TokenListView(LoginRequiredMixin, ListView):
    model = Token
    template_name = "django_opalstack/token_list.html"

    def get_queryset(self) -> QuerySet[Any]:
        qs = Token.objects.filter(user=self.request.user)
        return qs

    def get_template_names(self):
        if "Hx-Request" in self.request.headers:
            return ["django_opalstack/htmx/token_list.html"]
        return super().get_template_names()

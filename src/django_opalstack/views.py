from typing import Any

import opalstack
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.http import Http404
from django.views.generic import DetailView, ListView

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


class TokenDetailView(LoginRequiredMixin, DetailView):
    model = Token
    template_name = "django_opalstack/token_detail.html"

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

    def get_template_names(self):
        if "Hx-Request" in self.request.headers:
            return ["django_opalstack/htmx/token_detail.html"]
        return super().get_template_names()


class TokenServerDetailView(TokenDetailView):

    def get_template_names(self):
        if "Hx-Request" not in self.request.headers:
            raise Http404
        return ["django_opalstack/htmx/server_list.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opalapi = opalstack.Api(token=self.object.key)
        context["web_servers"] = opalapi.servers.list_all()["web_servers"]
        return context

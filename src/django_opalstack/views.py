from typing import Any

import opalstack
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.http import Http404
from django.views.generic import DetailView, ListView
from opalstack.util import filt, filt_one

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opalapi = opalstack.Api(token=self.object.key)
        context["web_servers"] = opalapi.servers.list_all()["web_servers"]
        return context

    def get_template_names(self):
        if "Hx-Request" in self.request.headers:
            return ["django_opalstack/htmx/token_detail.html"]
        return super().get_template_names()


class TokenServerDetailView(TokenDetailView):
    # TODO this view may be erased

    def get_template_names(self):
        if "Hx-Request" not in self.request.headers:
            raise Http404
        return ["django_opalstack/htmx/server_list.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opalapi = opalstack.Api(token=self.object.key)
        context["web_servers"] = opalapi.servers.list_all()["web_servers"]
        return context


class TokenUsersDetailView(TokenDetailView):

    def get_template_names(self):
        if "Hx-Request" not in self.request.headers:
            raise Http404
        return ["django_opalstack/htmx/user_list.html"]

    def get_context_data(self, **kwargs):
        if "server_id" not in self.request.GET:
            raise Http404
        context = super().get_context_data(**kwargs)
        opalapi = opalstack.Api(token=self.object.key)
        context["osusers"] = filt(
            opalapi.osusers.list_all(),
            {"server": self.request.GET["server_id"]},
        )
        return context


class TokenAppsDetailView(TokenDetailView):

    def get_template_names(self):
        if "Hx-Request" not in self.request.headers:
            raise Http404
        return ["django_opalstack/htmx/app_list.html"]

    def get_context_data(self, **kwargs):
        if "osuser_name" not in self.request.GET:
            raise Http404
        context = super().get_context_data(**kwargs)
        opalapi = opalstack.Api(token=self.object.key)
        context["apps"] = filt(
            opalapi.apps.list_all(),
            {
                "server": self.request.GET["server_id"],
                "osuser_name": self.request.GET["osuser_name"],
            },
        )
        return context


class TokenDomainsDetailView(TokenDetailView):

    def get_template_names(self):
        if "Hx-Request" not in self.request.headers:
            raise Http404
        return ["django_opalstack/htmx/domain_list.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opalapi = opalstack.Api(token=self.object.key)
        context["domains"] = opalapi.domains.list_all()
        return context


class TokenSitesDetailView(TokenDetailView):

    def get_template_names(self):
        if "Hx-Request" not in self.request.headers:
            raise Http404
        return ["django_opalstack/htmx/site_list.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opalapi = opalstack.Api(token=self.object.key)
        context["opal_sites"] = opalapi.sites.list_all(
            embed=["server", "domains", "primary_domain"]
        )
        return context


class TokenApplicationDetailView(TokenDetailView):

    def get_template_names(self):
        if "Hx-Request" not in self.request.headers:
            raise Http404
        return ["django_opalstack/htmx/app_detail.html"]

    def get_context_data(self, **kwargs):
        if "app_id" not in self.request.GET:
            raise Http404
        context = super().get_context_data(**kwargs)
        opalapi = opalstack.Api(token=self.object.key)
        context["app"] = filt_one(
            opalapi.apps.list_all(), {"id": self.request.GET["app_id"]}
        )
        return context

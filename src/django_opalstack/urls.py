from django.urls import path

from .views import (
    TokenAppsDetailView,
    TokenDetailView,
    TokenDomainsDetailView,
    TokenListView,
    TokenServerDetailView,
    TokenSitesDetailView,
    TokenUsersDetailView,
)

app_name = "django_opalstack"
urlpatterns = [
    path("token/", TokenListView.as_view(), name="token_list"),
    path("token/<pk>/", TokenDetailView.as_view(), name="token_detail"),
    path("token/<pk>/servers/", TokenServerDetailView.as_view(), name="server_list"),
    path("token/<pk>/users/", TokenUsersDetailView.as_view(), name="user_list"),
    path("token/<pk>/apps/", TokenAppsDetailView.as_view(), name="app_list"),
    path("token/<pk>/domains/", TokenDomainsDetailView.as_view(), name="domain_list"),
    path("token/<pk>/sites/", TokenSitesDetailView.as_view(), name="site_list"),
]

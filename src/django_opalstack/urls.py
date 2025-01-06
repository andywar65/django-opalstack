from django.urls import path

from .views import (
    TokenApplicationDetailView,
    TokenAppsDetailView,
    TokenDetailView,
    TokenListView,
    TokenSitesDetailView,
    TokenUsersDetailView,
)

app_name = "django_opalstack"
urlpatterns = [
    path("token/", TokenListView.as_view(), name="token_list"),
    path("token/<pk>/", TokenDetailView.as_view(), name="token_detail"),
    path("token/<pk>/users/", TokenUsersDetailView.as_view(), name="user_list"),
    path("token/<pk>/apps/", TokenAppsDetailView.as_view(), name="app_list"),
    path("token/<pk>/sites/", TokenSitesDetailView.as_view(), name="site_list"),
    path(
        "token/<pk>/application/",
        TokenApplicationDetailView.as_view(),
        name="app_detail",
    ),
]

from django.urls import path

from .views import TokenDetailView, TokenListView, TokenServerDetailView

app_name = "django_opalstack"
urlpatterns = [
    path("token/", TokenListView.as_view(), name="token_list"),
    path("token/<pk>/", TokenDetailView.as_view(), name="token_detail"),
    path("token/<pk>/servers/", TokenServerDetailView.as_view(), name="server_list"),
]

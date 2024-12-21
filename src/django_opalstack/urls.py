from django.urls import path

from .views import TokenListView

app_name = "django_opalstack"
urlpatterns = [
    path("token/", TokenListView.as_view(), name="token_list"),
]

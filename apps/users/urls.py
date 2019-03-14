from django.urls import path

from users.api.views import (
    FacebookLogin,
    GoogleLogin,
)

app_name = "users"
urlpatterns = [
    path("rest-auth/facebook/", FacebookLogin.as_view(), name='fb_login'),
    path("rest-auth/google/", GoogleLogin.as_view(), name='google_login'),
]

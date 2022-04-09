from django.urls import path

from proprietor.register.views import (
    AppLoginView,
    AppRegisterView,
    AddProfileView,
    AppLogoutView,
    ProfileDetailsView,
    login_success,
    EditProfileView,
    DeleteProfileView,
)

urlpatterns = [
    path("", AppRegisterView.as_view(), name="register"),
    path("login/", AppLoginView.as_view(), name="login"),
    path("login_success/", login_success, name="login success"),
    path("logout/", AppLogoutView.as_view(), name="logout"),
    path("profile/create", AddProfileView.as_view(), name="create profile"),
    path("profile/<int:pk>/view", ProfileDetailsView.as_view(), name="view profile"),
    path("profile/<int:pk>/edit", EditProfileView.as_view(), name="edit profile"),
    path("profile/<int:pk>/delete", DeleteProfileView.as_view(), name="delete profile"),
]

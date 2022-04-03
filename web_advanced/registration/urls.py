from django.urls import path

from web_advanced.registration.views import AppLoginView, AppRegisterView, AddProfileView, AppLogoutView, login_success, \
    EditProfileView, DeleteProfileView

urlpatterns = [
    path('', AppRegisterView.as_view(), name='sign-up'),
    path('login/', AppLoginView.as_view(), name='sign-in'),
    path('login_success/', login_success, name='login success'),
    path('profile/create', AddProfileView.as_view(), name='create profile'),
    path('profile/edit/<int:pk>', EditProfileView.as_view(), name='edit profile'),
    path('profile/delete/<int:pk>', DeleteProfileView.as_view(), name='delete profile'),
    path('logout/', AppLogoutView.as_view(), name='logout view'),
]

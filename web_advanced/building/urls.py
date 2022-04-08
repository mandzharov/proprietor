from django.urls import path

from web_advanced.building import views

urlpatterns = [
    path("", views.AllBuildingsView.as_view(), name="view buildings"),
    path("my_apartments/", views.MyApartmentsView.as_view(), name="view my apartments"),
    path("<int:pk>/create/", views.AllBuildingsView.as_view(), name="create building"),
    path("<int:pk>/edit/", views.AllBuildingsView.as_view(), name="edit building"),
    path("<int:pk>/delete/", views.AllBuildingsView.as_view(), name="delete building"),
    path("<int:pk>/apartment/", views.AllBuildingsView.as_view(), name="view apartments"),
    path("<int:pk>/apartment/<int:apt_pk>/create/", views.AllBuildingsView.as_view(), name="create apartment"),
    path("<int:pk>/apartment/<int:apt_pk>/edit/", views.AllBuildingsView.as_view(), name="edit apartment"),
    path("<int:pk>/apartment/<int:apt_pk>/delete/", views.AllBuildingsView.as_view(), name="delete apartment"),
]

from django.urls import path

from proprietor.building import views

urlpatterns = [
    path("", views.AllBuildingsView.as_view(), name="view buildings"),
    path("<int:pk>/create/", views.AllBuildingsView.as_view(), name="create building"),
    path("<int:pk>/edit/", views.AllBuildingsView.as_view(), name="edit building"),
    path("<int:pk>/delete/", views.AllBuildingsView.as_view(), name="delete building"),
    path("<int:pk>/apartment/", views.AllBuildingsView.as_view(), name="view apartments"),
    path("<int:pk>/apartment/<int:apt_pk>/create/", views.AllBuildingsView.as_view(), name="create apartment"),
    path("<int:pk>/apartment/<int:apt_pk>/edit/", views.AllBuildingsView.as_view(), name="edit apartment"),
    path("<int:pk>/apartment/<int:apt_pk>/delete/", views.AllBuildingsView.as_view(), name="delete apartment"),
    path("<int:pk>/apartment/<int:apt_pk>/expense/report/", views.ReportView.as_view(),
         name="report"),
    path("<int:pk>/apartment/<int:apt_pk>/expense/list/", views.ListUtilityExpensesView.as_view(),
         name="list expenses"),
    path("<int:pk>/apartment/<int:apt_pk>/expense/create/", views.AddUtilityExpenseView.as_view(), name="create expense"),
    path("<int:pk>/apartment/<int:apt_pk>/expense/<int:exp_pk>/edit/", views.EditUtilityExpenseView.as_view(),
         name="edit expense"),
    path("<int:pk>/apartment/<int:apt_pk>/expense/<int:exp_pk>/delete/", views.DeleteUtilityExpenseView.as_view(),
         name="delete expense"),
]

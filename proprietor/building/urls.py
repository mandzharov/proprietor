from django.urls import path

from proprietor.building import views
from proprietor.building.views import CreateUtilityView, EditUtilityView, DeleteUtilityView
from proprietor.views import ManagerAdminView

urlpatterns = [
    path("", views.AllBuildingsView.as_view(), name="view buildings"),
    path("admin/", ManagerAdminView.as_view(), name="manager admin"),
    path("utility/create/", CreateUtilityView.as_view(), name="create utility type"),
    path("utility/<int:pk>/edit/", EditUtilityView.as_view(), name="edit utility type"),
    path("utility/<int:pk>/delete/", DeleteUtilityView.as_view(), name="delete utility type"),
    path("<int:pk>/apartment/create/", views.AddApartmentView.as_view(), name="create apartment"),
    path("<int:pk>/apartment/<int:apt_pk>/edit/", views.EditApartmentView.as_view(), name="edit apartment"),
    path("<int:pk>/apartment/<int:apt_pk>/delete/", views.DeleteApartmentView.as_view(), name="delete apartment"),
    path("apartment/<int:apt_pk>/expense/report/", views.ReportView.as_view(),
         name="report"),

    path("apartment/<int:apt_pk>/expense/list/", views.ListUtilityExpensesView.as_view(),
         name="list expenses"),
    path("apartment/<int:apt_pk>/expense/create/", views.AddUtilityExpenseView.as_view(), name="create expense"),
    path("apartment/<int:apt_pk>/expense/<int:exp_pk>/edit/", views.EditUtilityExpenseView.as_view(),
         name="edit expense"),
    path("apartment/<int:apt_pk>/expense/<int:exp_pk>/delete/", views.DeleteUtilityExpenseView.as_view(),
         name="delete expense"),
]

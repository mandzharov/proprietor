from django.db.models import Avg
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as gen_views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core import exceptions

from proprietor.building.forms import (
    CreateExpenseForm,
    CreateUtilityForm,
    CreateApartmentForm,
)
from proprietor.building import helpers
from proprietor.building.models import (
    Apartment,
    Building,
    UtilitiesExpenses,
    UtilityType,
)


class AllBuildingsView(LoginRequiredMixin, PermissionRequiredMixin, gen_views.ListView):
    permission_required = "building.view_building"
    model = Building
    template_name = "building/all_buildings.html"


class MyApartmentsView(LoginRequiredMixin, gen_views.ListView):
    model = Apartment
    template_name = "building/my_apartments.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset


class ListUtilityExpensesView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    helpers.UtilityExpenseListViewMixin,
    gen_views.ListView,
):
    model = UtilitiesExpenses
    permission_required = "building.view_utilitiesexpenses"
    template_name = "building/expenses_list.html"
    paginate_by = 10


class AddUtilityExpenseView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    helpers.UtilityExpenseCreateViewMixin,
    gen_views.CreateView,
):
    model = UtilitiesExpenses
    permission_required = "building.add_utilitiesexpenses"
    template_name = "building/add_expense.html"
    form_class = CreateExpenseForm


class EditUtilityExpenseView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    helpers.UtilityExpenseEditViewMixin,
    gen_views.UpdateView,
):
    model = UtilitiesExpenses
    permission_required = "building.change_utilitiesexpenses"
    template_name = "building/add_expense.html"
    fields = ["utility_type", "amount", "bill_year", "bill_month"]


class DeleteUtilityExpenseView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    helpers.UtilityExpenseDeleteViewMixin,
    gen_views.DeleteView,
):
    model = UtilitiesExpenses
    permission_required = "building.delete_utilitiesexpenses"
    template_name = "building/delete_expense.html"


class ReportView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    helpers.ApartmentDispatchMixin,
    gen_views.View,
):
    http_method_names = ["get"]
    permission_required = "building.view_utilitiesexpenses"

    def get(self, request, *args, **kwargs):
        queryset = UtilitiesExpenses.objects.filter(apartment_id=self.kwargs["apt_pk"])
        year_selected = "All"
        month_selected = "All"
        type_selected = "All"
        if request.GET:
            year_selected = request.GET.get("Year")
            month_selected = request.GET.get("Month").strip()
            type_selected = request.GET.get("Type")
        if not year_selected == "All":
            queryset = queryset.filter(bill_year=year_selected)
        if not month_selected == "All":
            queryset = queryset.filter(bill_month=month_selected)
        if not type_selected == "All":
            queryset = queryset.filter(utility_type__name=type_selected)
        year_choices = (
            queryset.order_by("bill_year").values_list("bill_year").distinct()
        )
        month_choices = (
            queryset.order_by("bill_month").values_list("bill_month").distinct()
        )
        type_choices = (
            queryset.order_by("utility_type__name")
            .values_list("utility_type__name")
            .distinct()
        )
        result = queryset.aggregate(Avg("amount"))
        context = {
            "year_choices": [str(i[0]) for i in year_choices],
            "month_choices": [i[0] for i in month_choices],
            "type_choices": [i[0] for i in type_choices],
            "year_selected": year_selected,
            "month_selected": month_selected,
            "type_selected": type_selected,
            "result": result["amount__avg"],
            "apt_pk": self.kwargs["apt_pk"],
        }
        return render(request, template_name="building/report.html", context=context)


class CreateUtilityView(
    LoginRequiredMixin, PermissionRequiredMixin, gen_views.CreateView
):
    model = UtilityType
    permission_required = "building.add_utilitytype"
    template_name = "building/add_utility_type.html"
    form_class = CreateUtilityForm
    success_url = reverse_lazy("manager admin")


class EditUtilityView(
    LoginRequiredMixin, PermissionRequiredMixin, gen_views.UpdateView
):
    model = UtilityType
    permission_required = "building.change_utilitytype"
    template_name = "building/add_utility_type.html"
    form_class = CreateUtilityForm
    success_url = reverse_lazy("manager admin")


class DeleteUtilityView(
    LoginRequiredMixin, PermissionRequiredMixin, gen_views.DeleteView
):
    model = UtilityType
    permission_required = "building.delete_utilitytype"
    template_name = "building/delete_utility.html"
    success_url = reverse_lazy("manager admin")


class AddApartmentView(
    LoginRequiredMixin, PermissionRequiredMixin, gen_views.CreateView
):
    model = Apartment
    permission_required = "building.add_apartment"
    template_name = "building/add_apartment.html"
    form_class = CreateApartmentForm
    success_url = reverse_lazy("manager admin")

    def dispatch(self, request, *args, **kwargs):
        building = Building.objects.get(pk=self.kwargs["pk"])
        if not building.manager == self.request.user:
            raise exceptions.PermissionDenied("You don't have permissions to do that")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        building_pk = self.kwargs["pk"]
        building = Building.objects.get(pk=building_pk)
        form_kwargs = super().get_form_kwargs()
        form_kwargs["building"] = building
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["building_pk"] = self.kwargs["pk"]
        return context


class EditApartmentView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    helpers.ApartmentEditDeleteViewMixin,
    gen_views.UpdateView,
):
    model = Apartment
    permission_required = "building.change_apartment"
    template_name = "building/add_apartment.html"
    success_url = reverse_lazy("manager admin")
    fields = ["floor", "number", "area", "rooms_count", "share", "description", "owner"]


class DeleteApartmentView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    helpers.ApartmentEditDeleteViewMixin,
    gen_views.DeleteView,
):
    model = Apartment
    permission_required = "building.delete_apartment"
    template_name = "building/delete_apartment.html"
    success_url = reverse_lazy("manager admin")

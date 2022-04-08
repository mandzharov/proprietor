from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import generic as gen_views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from web_advanced.building.models import Apartment, Building


class AllBuildingsView(LoginRequiredMixin, PermissionRequiredMixin, gen_views.ListView):
    permission_required = 'building.view_building'
    model = Building
    template_name = 'building/all_buildings.html'


class MyApartmentsView(LoginRequiredMixin, gen_views.ListView):
    model = Apartment
    template_name = 'building/my_apartments.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

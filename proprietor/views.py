from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic as gen_views

from proprietor.building.models import Building, Apartment, UtilityType
from proprietor.register.models import Profile

AppUser = get_user_model()


class HomePageView(gen_views.ListView):
    queryset = Building.objects.all()
    template_name = 'home_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        manager_ids = Building.objects.filter(manager__isnull=False).values_list('manager_id').distinct()
        managers = Profile.objects.filter(user__in=manager_ids)
        context.update({'managers_list': managers})
        return context


class ManagerAdminView(LoginRequiredMixin, gen_views.ListView):
    template_name = 'manager_admin.html'
    paginate_by = 1
    # paginate_orphans = 0

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home page')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        my_buildings_queryset = Building.objects.filter(manager=self.request.user)
        assigned_users = Apartment.objects.filter(owner__isnull=False).values_list('owner').distinct()
        pending_users_queryset = AppUser.objects.exclude(pk__in=assigned_users)
        utility_types_queryset = UtilityType.objects.all()

        return my_buildings_queryset, pending_users_queryset, utility_types_queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        my_buildings_queryset, pending_users_queryset, utility_types_queryset = self.object_list
        page_size = self.get_paginate_by(my_buildings_queryset)
        context = {
            'pending_users_list': pending_users_queryset,
            'my_buildings_list': my_buildings_queryset,
            'utility_types': utility_types_queryset
        }
        if page_size:
            paginator, page, my_buildings_queryset, is_paginated = self.paginate_queryset(
                my_buildings_queryset, page_size
            )
            context.update(
                {
                    "paginator": paginator,
                    "page_obj": page,
                    "is_paginated": is_paginated,
                    "object_list": my_buildings_queryset,
                }
            )
        else:
            context.update(
                {
                    "paginator": None,
                    "page_obj": None,
                    "is_paginated": False,
                    "object_list": my_buildings_queryset,
                }
            )
        context.update(kwargs)
        context.setdefault("view", self)
        return context

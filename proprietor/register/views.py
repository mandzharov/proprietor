from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as gen_views
from django.contrib.auth import views as auth_views
from django.contrib.auth import mixins as auth_mixins

from proprietor.register.forms import RegistrationForm, CreateProfileForm, LoginForm
from proprietor.register.models import Profile

AppUserModel = get_user_model()


class AppLoginView(auth_views.LoginView):
    next_page = reverse_lazy('login success')
    authentication_form = LoginForm
    template_name = 'register/login.html'


def login_success(request):
    if Profile.objects.filter(pk=request.user.pk):
        return redirect("home page")
    else:
        return redirect("create profile")


class AppLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('home page')


class AppRegisterView(gen_views.CreateView):
    template_name = 'register/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login success')

    def form_valid(self, form):
        form.save()
        email = self.request.POST['email']
        password = self.request.POST['password1']
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return redirect(self.success_url)


class ProfileDetailsView(gen_views.DetailView):
    model = Profile
    context_object_name = 'profile'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


class AddProfileView(auth_mixins.LoginRequiredMixin, gen_views.CreateView):
    form_class = CreateProfileForm
    template_name = 'register/profile.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self) -> str:
        user_pk = self.request.user.pk
        url = reverse_lazy('view profile', kwargs={'pk': user_pk})
        return url


class EditProfileView(auth_mixins.LoginRequiredMixin, gen_views.UpdateView):
    template_name = 'register/profile.html'
    model = Profile
    fields = [
        'first_name',
        'middle_name',
        'last_name',
        'birth_date',
        'gender',
        'picture',
        'phone_code',
        'phone',
    ]

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset
    
    def get_success_url(self) -> str:
        user_pk = self.request.user.pk
        url = reverse_lazy('view profile', kwargs={'pk': user_pk})
        return url


class DeleteProfileView(auth_mixins.LoginRequiredMixin, gen_views.DeleteView):
    model = AppUserModel
    success_url = reverse_lazy('home page')
    template_name = 'register/delete_profile.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(pk=self.request.user.pk)
        return queryset

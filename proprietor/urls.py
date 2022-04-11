from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from proprietor.building.views import MyApartmentsView
from proprietor.views import HomePageView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', HomePageView.as_view(template_name='home_page.html'), name='home page'),
                  path('register/', include('proprietor.register.urls')),
                  path('building/', include('proprietor.building.urls')),
                  path("my_apartments/", MyApartmentsView.as_view(), name="my apartments"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

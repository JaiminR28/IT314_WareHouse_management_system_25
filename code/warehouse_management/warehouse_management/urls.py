from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('base/', include('base.urls')),
    path('farmer/', include('farmer.urls')),    
    path('warehouse/', include('warehouse.urls')),    
    path('', RedirectView.as_view(url='home/home/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



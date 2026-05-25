from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('auth/', include('core.urls_auth')),
    path('dashboard/', include('core.urls_dashboard')),
    path('api/', include('core.urls_api')),
]

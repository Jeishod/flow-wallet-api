from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djadmin.api.urls')),
]

admin.site.site_header = settings.PROJECT_NAME

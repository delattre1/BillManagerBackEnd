from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bills.urls')),
]

if setting.DEBUG:
    urlpatterns += static(setting.STATIC_URL,
                          document_root=settings.STATIC_URL)


from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include('accounts.urls'), name="register"),
    path('api/', include('api.urls')),
    path('', include('frontend.urls')),   
]

# # Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

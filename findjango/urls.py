from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# main project urls
urlpatterns = [
    # django admin panel
    path('admin/', admin.site.urls),

    # all tracker app urls
    path('', include('tracker.urls')),
]

# serve media and static files in development
# in production a proper web server handles this
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

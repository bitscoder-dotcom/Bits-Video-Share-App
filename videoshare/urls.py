from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from videoshare.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', home_view, name='home'),  # Root URL points to home.html

    path('', include('content.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

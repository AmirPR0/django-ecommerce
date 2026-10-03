from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from accounts.views import CustomPasswordChangeView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom password change URL
    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),

    # URLs for allauth authentication
    path('accounts/', include('allauth.urls')),

    path('', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
)
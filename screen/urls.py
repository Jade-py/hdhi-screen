from django.contrib import admin
from django.urls import path
from base.views import trigger_action, show_screen
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_screen),
    path('set/', trigger_action, name='trigger_action'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

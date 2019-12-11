from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('froala_editor/', include('froala_editor.urls')),
    path('register/', user_views.register, name='register'),
    path('activate/<uidb64>/<token>/', user_views.activate, name='activate'),
    path('activate/done/', user_views.activate_done, name='activate-done'),
    path('', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

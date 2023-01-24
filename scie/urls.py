from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings

from apps.users.views import Login, Logout, UserToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name = 'login'),
    path('refresh-token/', UserToken.as_view(), name = 'refresh-token'),
    path('logout/', Logout.as_view(), name = 'logout'),
    path('users/', include('apps.users.api.routers')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
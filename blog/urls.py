from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from core.views import Home,blog,Post_list,search,post_update,post_delete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home),
    path('post/<id>', blog,name='page'),
    path('post/', Post_list,name='post-list'),
    path('search/', search,name='search'),
    path('post/<id>/update', post_update,name='post-update'),
    path('post/<id>/delete', post_delete,name='post-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

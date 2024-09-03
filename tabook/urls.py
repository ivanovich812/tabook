from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path("", views.index),
    path('create_melody/', views.create_melody),
    path('delete_melody/<int:id>/', views.delete_melody),
    path('show_melody/<int:id>/', views.show_melody),
    path('edit_melody/<int:id>/', views.edit_melody),
    path('add_url/<int:id>/', views.add_url),
    path('delete_url/<int:melody_id>/<int:url_id>', views.delete_url),
    path('add_image/<int:id>/', views.add_image),
    path('delete_image/<int:melody_id>/<int:image_id>', views.delete_image),
    path('edit_image/<int:melody_id>/<int:image_id>/', views.edit_image),
    path('add_tab/<int:id>/', views.add_tab),
    path('delete_tab/<int:melody_id>/<int:tab_id>', views.delete_tab),
    path('edit_tab/<int:melody_id>/<int:tab_id>/', views.edit_tab),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

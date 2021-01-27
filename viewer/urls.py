from django.urls import path

from . import views

urlpatterns = [
    path('', views.listfolder, name='index'),
    path('folder/<path:url>/', views.listfolder, name='folder'),
    path('file/<path:name>', views.download, name='file'),
]

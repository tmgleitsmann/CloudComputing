from django.urls import path
from . import views

urlpatterns = [
	path('', views.DN_home, name='DN_app_home'),
	path('GET/', views.get, name='DN_app_get'),
	path('POST/', views.post, name='DN_app_post'),
]

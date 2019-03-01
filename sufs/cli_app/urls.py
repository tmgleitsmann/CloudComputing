from django.urls import path
from . import views

urlpatterns = [
	path('', views.cli_home, name='cli_app_home'),
	path('GET/', views.get, name='cli_app_get'),
	path('POST/', views.post, name='cli_app_post'),
]

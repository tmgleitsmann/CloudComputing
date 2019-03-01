from django.urls import path
from . import views

urlpatterns = [
	path('', views.NN_home, name='NN_app_home'),
	path('GET/', views.get, name='NN_app_get'),
	path('POST/', views.post, name='NN_app_post'),
]

from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='app-home'),
	path('GET/', views.get, name='app-get'),
	path('POST/', views.post, name='app-post'),
]

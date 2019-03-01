from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
	#define what happens during route call.
	return HttpResponse('<h1>Home functionality<h1>')

def get(request):
	return HttpResponse('<h1>GET functionality<h1>')

def post(request):
	return HttpResponse('<h1>POST functionality<h1>')
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def cli_home(request):
	#define what happens during route call.
    cli_message = "hello from the client!"
	return HttpResponse('<h1>Client Home<h1>')


def get(request):
	#define what happens during route call.
	return HttpResponse('<h1>GET<h1>')


def post(request):
	#define what happens during route call.
	return HttpResponse('<h1>POST<h1>')

# Create your views here.

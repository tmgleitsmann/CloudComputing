from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def cli_home(request):
    # cli_message = "hello from the client!"
    # data = {'foo':'bar'}
    data = "some cool data"
    return HttpResponse(data)


def get(request):
	#define what happens during route call.
	return HttpResponse('<h1>Cli GET<h1>')


def post(request):
	#define what happens during route call.
	return HttpResponse('<h1>Cli POST<h1>')

# Create your views here.

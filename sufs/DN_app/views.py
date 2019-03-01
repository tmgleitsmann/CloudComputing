from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def DN_home(request):
    # cli_message = "hello from the client!"
    # data = {'foo':'bar'}
    data = "Hello from the DN"
    return HttpResponse(data)

def get(request):
	#define what happens during route call.
	return HttpResponse('<h1>DN GET<h1>')


def post(request):
	#define what happens during route call.
	return HttpResponse('<h1>DN POST<h1>')

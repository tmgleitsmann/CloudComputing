from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def cli_home(request):

    data = request.META

    # # cli_message = "hello from the client!"
    # # data = {'foo':'bar'}
    # data = "some cool data"
    return HttpResponse(data)


def get(request):
	#define what happens during route call.
	return HttpResponse('<h1>Cli GET<h1>')


def post(request):
	#define what happens during route call.
	return HttpResponse('<h1>Cli POST<h1>')

def post_NN(request, size, data1, NNIPAdress):
	#we need a post request from here to the NN.
	
	#we want to await a response before we return a value to client.py
	return 'sufs.cli_app.views.post_NN() was called upon'
# Create your views here.

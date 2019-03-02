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

def post_NN(request, size, data1, NNIPAddress):
	#we need a post request from here to the NN.
	callback_val = request.post(NNIPAddress, data1)
	#we want to await a response before we return a value to client.py
	return callback_val
# Create your views here.

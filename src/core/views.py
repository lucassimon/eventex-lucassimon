# Create your views here.


from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime

def homepage(request):
	dataAtual = datetime.datetime.now()
	dataInscricao = datetime.datetime(2012,03,18,9,00,00,00)
	context = RequestContext(request)
	return render_to_response('index.html',locals(),context)

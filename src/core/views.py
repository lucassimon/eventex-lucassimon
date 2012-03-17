# Create your views here.


from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime

def homepage(request):
	dataAtual = datetime.datetime.now()
	dataInscricao = datetime.date(2012,03,18)
	context = RequestContext(request)
	return render_to_response('index.html',locals(),context)

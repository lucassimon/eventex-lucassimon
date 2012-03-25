# Create your views here.


from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime

def homepage(request,template=None):
	""" Action para exibir a home do site """
	dataAtual = datetime.datetime.now()
	dataInscricao = datetime.datetime(2012,03,18,9,00,00,00)
	context = RequestContext(request)
	return render_to_response(template,locals(),context)

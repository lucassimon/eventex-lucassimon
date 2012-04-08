# Create your views here.


from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import datetime
from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView
from core.models import Speaker, Talk


class HomepageView(TemplateView):
	"""docstring for HomepageView"""
	template_name = 'index.html'

def homepage(request,template=None):
	""" Action para exibir a home do site """
	dataAtual = datetime.datetime.now()
	dataInscricao = datetime.datetime(2012,03,18,9,00,00,00)
	context = RequestContext(request)
	return render_to_response(template,locals(),context)


def speaker_detail(request,slug):
	speaker = get_object_or_404(Speaker, slug=slug)
	context = RequestContext(request, {'speaker': speaker})
	return render_to_response('core/speaker_detail.html', context)


def talks(request):
	return direct_to_template(request,'core/talks.html',
		{
			'morning_talks': Talk.objects.at_morning(),
			'afternoon_talks': Talk.objects.at_afternoon()
		}
	)


def talk_detail(request,talk_id):
	talk = get_object_or_404(Talk,id=talk_id)
	return direct_to_template(request, 'core/talk_detail.html',
		{
			'talk': talk,
			'slides': talk.media_set.filter(type="SL"),
			'videos': talk.media_set.filter(type="YT"),
		}
	)
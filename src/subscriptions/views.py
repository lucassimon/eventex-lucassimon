# Create your views here.
# encoding: utf-8 
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from forms import SubscriptionForm
from django.core.urlresolvers import reverse, resolve
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from subscriptions.models import Subscription

def subscribe(request):
	""" Action para exibir o formulario para o usuario """ 
	if request.method == 'POST':
		return createSubscribe(request)
	else:
		return getSubscribe(request)


def getSubscribe(request):
	form = SubscriptionForm(initial = {
		'name': 'Entre com seu nome',
		'cpf': 'Digite o seu CPF sem pontos',
		'email': 'seuemail@email.com',
		'phone': '',
	})
	context = RequestContext(request, {'form': form})
	return render_to_response('subscriptions/new.html',context)


def createSubscribe(request):
	form = SubscriptionForm(request.POST)

	if not form.is_valid():
		context = RequestContext(request, {'form': form})
		return render_to_response('subscriptions/new.html',context)

	subscription = form.save(commit = False)
	subscription.email = form.cleaned_data['email'] or None
	# A linha acima significa:
	# if form.cleaned_data['email']:
	# 		subscription.email = form.cleaned_data['email']
	# else:
	# 		subscription.email = None

	# Salva definitivamente o objeto no banco
	subscription.save()

	# caso nao tenha email, nao envia a mensagem
	if subscription.email:
		send_confirmation(subscription.email)

	return HttpResponseRedirect(reverse('subscriptions:success',args=[subscription.pk]))


def success(request, pk):
	subscription = get_object_or_404(Subscription, pk=pk)
	context = RequestContext(request, {'subscription':subscription})
	return render_to_response('subscriptions/success.html',context)


def send_confirmation(email):
	""" Enviando email para o usuario apos salvar os dados"""
	send_mail(subject=u'Cadastrado com sucesso',
		message='Obrigado pela sua inscrição!',
		from_email = settings.DEFAULT_FROM_EMAIL,
		recipient_list = [email]
	)

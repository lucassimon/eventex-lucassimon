# encoding: utf-8 
from django.db import models

# Create your models here.

class Subscription(models.Model):
	"""Classe para model de subscricao do evento
		A instancia de um subscription salva apenas 01 linha na tabela.
	"""
	name       = models.CharField(max_length=100)
	cpf        = models.CharField(max_length=11, unique=True)
	email      = models.EmailField(unique=True)
	phone      = models.CharField(max_length=20, blank=True)
	""" Gravar com a data e hora atual """
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

	class Meta:
		"""Definindo o dicionario de dados para que a leitura dos campos seja em formato humano, e configurar o padrao do querySet"""
		ordering            = ["created_at"]
		verbose_name        = "Inscrição"
		verbose_name_plural = "Inscrições"
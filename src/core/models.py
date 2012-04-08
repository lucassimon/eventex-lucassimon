# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
import datetime

# Create your models here.

# Abstract Base Class
# class Session(models.Model):
# 	"""docstring for Session"""
# 	title       = models.CharField(max_length=200)
# 	description = models.TextField()
# 	start_time  = models.TimeField(blank=True)
# 	objects     = PeriodManager()
# 	class Meta:
# 		abstract = True

# 	def __unicode__(self):
# 		return unicode(self.title)

class Speaker(models.Model):
	"""Classe model para o speaker"""
	name        = models.CharField(max_length=255)
	slug        = models.SlugField(unique=True)
	url         = models.URLField(verify_exists = False)
	description = models.TextField(blank = True)
	avatar      = models.FileField(upload_to='palestrantes',blank=True,null=True)

	def __unicode__(self):
		return self.name

class kindContactManager(models.Manager):
	"""docstring for kindContactManager"""
	def __init__(self, kind):
		super(kindContactManager, self).__init__()
		self.kind = kind
		def get_query_set(self):
			qs = super(PhoneContactManager,self).get_query_set()
			qs = qs.filter(kind=self.kind)
			return qs

class Contact(models.Model):
	"""Classe para o contato"""
	KINDS = (
		('P',_('Telefone')),
		('E',_('E-mail')),
		('F',_('Fax')),
	)
	speaker = models.ForeignKey('Speaker', verbose_name=_('Palestrante') )
	kind    = models.CharField(_(u'Tipo'),max_length=1, choices=KINDS)
	value   = models.CharField(_(u'Valor'),max_length=255)
	
	objects = models.Manager()
	phones  = kindContactManager('P')
	emails  = kindContactManager('E') 
	faxes   = kindContactManager('F')
	class Meta:
		verbose_name = _(u'Contato')
	def __unicode__(self):
		return u'%s, %s' % (self.kind, self.value)

class PeriodManager(models.Manager):
	"""docstring for PeriodManager"""
	midday = datetime.time(12)

	def at_morning(self):
		qs = self.filter(start_time__lt=self.midday)
		qs = qs.order_by('start_time')
		return qs

	def at_afternoon(self):
		qs = self.filter(start_time__gte=self.midday)
		qs = qs.order_by('start_time')
		return qs

class Talk(models.Model):
	""" """
	title       = models.CharField(_(u'Titulo'),max_length=200)
	description = models.TextField(_(u'Descrição'),blank=True )
	start_time  = models.TimeField(_(u'Horário'),blank=True)
	speakers    = models.ManyToManyField('Speaker',verbose_name=_('palestrante'))
	
	objects     = PeriodManager()

	class Meta:
		verbose_name = _(u'Palestra')

	@property
	def slides(self):
		return self.media_set.filter(type='SL')

	@property
	def videos(self):
		return self.media_set.filter(type='YT')

	def __unicode__(self):
		return unicode(self.title)

class Course(Talk):
	"""docstring for Course"""
	slots   = models.IntegerField()
	notes   = models.TextField()
	objects = PeriodManager()
	class Meta:
		verbose_name = _(u'Curso')

class CodingCourse(Course):
    class Meta:
        proxy = True
    def do_some_python_stuff(self):
        return "Let's hack! at %s" % self.title

class Media(models.Model):
	"""docstring for Me"""
	MEDIAS = (
		('SL','SlideShare'),
		('YT','YouTube'),
	)
	talk = models.ForeignKey('Talk')
	type = models.CharField(max_length=3,choices=MEDIAS)
	title = models.CharField(_(u'Titulo'),max_length=255)
	media_id = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s - %s' % (self.talk.title, self.title)

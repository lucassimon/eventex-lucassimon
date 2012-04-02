# encoding: utf-8 
import datetime
from django.contrib import admin
from subscriptions.models import Subscription
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.http import HttpResponse
from django.conf.urls.defaults import patterns, url
import csv

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'subscribed_today','paid')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'cpf', 'email', 'phone', 'created_at')

    list_filter = ('created_at','paid',)
    #list_filter = ('paid',)

    actions = ['mark_as_paid']

    def subscribed_today(self, obj):
        return obj.created_at.date() == datetime.date.today()

    subscribed_today.short_description = _(u'Inscrito hoje?')
    subscribed_today.boolean = True


    def mark_as_paid(self,request,queryset):
    	count = queryset.update(paid = True)
    	msg = ungettext(
    		u'%(count)d inscrição foi marcada como paga.',
    		u'%(count)d inscrições foram marcadas como pagas.',
    		count
    	) % {'count' : count}
    	self.message_user(request,msg)

    mark_as_paid.short_description = _(u'Marcar como pagas')
    #paid.short_description = _(u'Pago?')

    def export_subscriptions(self,request):
    	# coloca o mimetype da pagina para text/csv
    	response = HttpResponse(mimetype='text/csv')
    	# vai ser por download e o nome do arquivo sera listaInscricao
    	response['Content-Disposition'] = 'attachment; filename=listaInscricao.csv'
    	# resgata todos os objetos do model correte(subscription)
    	subscriptions = self.model.objects.all()
    	# inicializa a tupla vazia
    	tuplaWriteCsv = ()
    	# inicializa a tupla temporaria
    	tempTupla = ()
    	# arquivo para fazer escrita das tupla original, formato csv
    	out = csv.writer(response)
    	# faz a interacao do queryset subscriptions acima
    	for s in subscriptions:
    		# cria uma tupla contendo o nome,cpf,email,phone,criado em, e pago
    		tempTupla = (s.name,s.cpf,s.email,s.phone)
    		# coloca na tupla oficial o conteudo da tupla temporaria sempre adicionando uma virgula no final
    		tuplaWriteCsv += tempTupla,
    	# escrevendo as tuplas no arquivo
    	out.writerows(tuplaWriteCsv)
    	# retorna o response 
    	return response


    def get_urls(self):
    	original_urls = super(SubscriptionAdmin,self).get_urls()
    	extra_url = patterns('',
    		url(r'exportar-inscricoes/$', 
    			self.admin_site.admin_view(self.export_subscriptions),
    			name = 'export_subscriptions'
    		)
    	)
    	return extra_url + original_urls


admin.site.register(Subscription, SubscriptionAdmin)
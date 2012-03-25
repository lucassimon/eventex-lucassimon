from django.conf.urls.defaults import patterns, include, url
from core.views import homepage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('django.views.generic.simple',
    # Examples:
    # url(r'^$', 'src.views.home', name='home'),
    # url(r'^src/', include('src.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^admin/', include('django.contrib.admin.urls')),

    # Generalizando as views passando como parametro qual template vou usar
    url(r'^$','direct_to_template', {'template': 'index.html'}),

    #url(r'^$', 'direct_to_template', {'template':'index.html'})
    url(r'^inscricao/',include('subscriptions.urls',namespace='subscriptions')),
)


urlpatterns += staticfiles_urlpatterns()
from django.conf.urls.defaults import patterns, url
from views import HomepageView


urlpatterns = patterns(
	'core.views',
	url(r'^$',HomepageView.as_view(),name='homepage'),
	url(r'^palestras/$', 'talks', name='talks' ),
	url(r'^palestras/(\d+)/$', 'talk_detail', name='talk_detail' ),
	url(r'^palestrante/([-\w]+)/$', 'speaker_detail', name='speaker_detail' ),

)
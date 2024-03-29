from django.conf.urls.defaults import patterns, url
from views import HomepageView
from views import TalkDetailView
from views import TalkListView
from views import SpeakerDetailView


urlpatterns = patterns(
	'core.views',
	url(r'^$',HomepageView.as_view(),name='homepage'),
	url(r'^palestras/$', TalkListView.as_view(), name='talks' ),
	url(r'^palestras/(?P<pk>\d+)/$', TalkDetailView.as_view(), name='talk_detail' ),
	url(r'^palestrante/(?P<slug>[-\w]+)/$', SpeakerDetailView.as_view(), name='speaker_detail' ),

)
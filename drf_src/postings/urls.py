from django.conf.urls import url

from postings.api import views

urlpatterns = [
	url(r'^(?P<pk>\d+)/$', views.BlogPostRudView.as_view(), name='post-rud'),
	url(r'^$', views.BlogPostAPIView.as_view(), name='post-listcreate'),
]
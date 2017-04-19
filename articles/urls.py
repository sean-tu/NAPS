from django.conf.urls import url
from . import views as articles_views

urlpatterns = [
	url(r'^accounts/signup/$', articles_views.signup, name='signup'),
    url(r'^articles/$', articles_views.article_list, name='article_list'),
    url(r'^articles/upload/$', articles_views.upload_pdf, name='upload_pdf'),
    url(r'^articles/(?P<pk>\d+)/edit$', articles_views.article_update, name='article_update'),
    url(r'^articles/(?P<pk>\d+)/delete$', articles_views.article_delete, name='article_delete'),
    url(r'^articles/(?P<pk>\d+)/$', articles_views.article_detail, name='article_detail'),
    url(r'^about/$', articles_views.about, name='about'),
    url(r'^help/$', articles_views.help, name='help'),
    url(r'^$', articles_views.home, name='home')
]
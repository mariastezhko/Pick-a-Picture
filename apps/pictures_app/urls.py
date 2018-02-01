from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^upload/?$', views.renderForm), # '?' is to indicate that '/' is optional
    url(r'^submitcriteria/?$', views.submitCriteria),
    url(r'^submitsubcategory/?$', views.submitSubcategory),
    url(r'^submitimage/?$', views.submitImage),
    #url(r'^process/?$', views.processAnswer),

]

from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    url(r'(?P<hashid>[0-9a-zA-Z]+)$', 'paste.views.view_paste', name='view_paste'),
]

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from views.registration_views import *
from views.dashboard_views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^register/$', register, name='register'),
    url(r'^confirm-registration/(?P<user_id>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        confirm_registration, name='confirm-registration'),
    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'registration/confirm_email.html'},
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'registration/email_sent.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'registration/password_reset.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'registration/password_reset_success.html'},
        name='password_reset_complete'),
    url(r'^change-password$', change_password, name='change-password'),

    url(r'^$', dashboard, name='dash'),
]

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as kairos_views

urlpatterns = [
    url(r'^$', kairos_views.dashboard, name='dash'),

    url(r'^login/$', kairos_views.login, name='login'),
    url(r'^logout$', kairos_views.logout_user, name='logout'),

    url(r'^register/$', kairos_views.register, name='register'),
    url(r'^confirm-registration/(?P<user_id>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        kairos_views.confirm_registration, name='confirm-registration'),
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
    url(r'^change-password$', kairos_views.change_password, name='change-password'),

    url(r'^(?P<user_id>\d+)/edit-profile/$', kairos_views.edit_profile, name='edit-profile'),
]

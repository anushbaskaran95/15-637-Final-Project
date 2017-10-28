from django.conf.urls import url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from views.registration import *
from views.dashboard import *
from views.login import *
from views.currenttasks import *
from views.coursework import *
from views.research import *
from views.routine import *
from views.profile import *

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^confirm-registration/(?P<user_id>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        confirm_registration, name='confirm-registration'),
    url(r'^password_reset/$', password_reset, {'template_name': 'registration/confirm_email.html',
                                               'post_reset_redirect': 'password_reset_done'}, name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done, {'template_name': 'registration/reset_link_sent.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {'template_name': 'registration/password_reset.html', 'post_reset_redirect': 'password_reset_complete'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete,
        {'template_name': 'registration/password_reset_success.html'},
        name='password_reset_complete'),
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^$', dashboard, name='dash'),
    url(r'^current-tasks$', current_tasks, name='currenttasks'),
    url(r'^course-work$', coursework, name='coursework'),
    url(r'^research$', research, name='research'),
    url(r'^routine$', dashboard, name='routine'),
    url(r'^profile$', edit_student_profile, name='profile'),
]

from django.conf.urls import url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete
from views.registration import *
from views.dashboard import *
from views.login import *
from views.coursework import *
from views.research import *
from views.routine import *
from views.profile import *
from views.buttonprocess import *
from views.get_task_info import *
from views.get_notification import *
from views.analytics import *

urlpatterns = [
    url(r'^register$', register, name='register'),
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

    url(r'^login$', login_user, name='login'),
    url(r'^logout$', logout_user, name='logout'),

    url(r'^$', dashboard, name='dash'),
    url(r'^course-work$', coursework, name='coursework'),
    url(r'^research$', research, name='research'),
    url(r'^routine$', routine, name='routine'),

    url(r'^edit-profile/(?P<user_id>\d+)$', edit_profile, name='edit-profile'),
    url(r'^change-password$', change_password, name='change-password'),

    url(r'^add-course$', add_course, name='add-course'),
    url(r'^add-course-task$', add_course_task, name='add-course-task'),
    url(r'^add-research-task$', add_research_task, name='add-research-task'),
    url(r'^add-routine-task$', add_routine_task, name='add-routine-task'),

    url(r'^edit-course-modal/(?P<task_id>\d+)/(?P<task_info_id>\d+)$', edit_course_modal,
        name='edit-course-modal'),
    url(r'^edit-research-modal/(?P<task_id>\d+)/(?P<task_info_id>\d+)$', edit_research_modal,
        name='edit-research-modal'),
    url(r'^edit-routine-modal/(?P<task_id>\d+)/(?P<task_info_id>\d+)$', edit_routine_modal,
        name='edit-routine-modal'),
    url(r'^button_process$', process_button, name='process_button'),
    url(r'^stop_process$', process_stop, name='process_stop'),

    url(r'^edit-course-task$', edit_course_task, name='edit-course-task'),
    url(r'^edit-research-task$', edit_research_task, name='edit-research-task'),
    url(r'^edit-routine-task$', edit_routine_task, name='edit-routine-task'),
    url(r'^get-task-info$', get_task_info, name='get-task-info'),

    url(r'^get-notification-expected-finish$', get_notification_expected_finish, name='get-notification-expected-finish'),
    url(r'^get-notification-due$', get_notification_due, name='get-notification-due'),

    url(r'^analytics$', analytics, name='analytics'),
    url(r'^course-analytics$', course_analytics, name='course-analytics'),
    url(r'^research-analytics$', research_analytics, name='research-analytics'),
    url(r'^overall-analytics$', overall_analytics, name='overall-analytics'),

    url(r'^get-course-analytics$', get_course_analytics, name='get-course-analytics'),
    url(r'^get-research-analytics$', get_research_analytics, name='get-research-analytics'),
    url(r'^get-overall-analytics$', get_overall_analytics, name='get-overall-analytics'),
    url(r'^get-tree-analytics$', get_tree_analytics, name='get-tree-analytics'),
    url(r'^get-on-time-late-tasks$', get_on_time_late_tasks, name='get-on-time-late-tasks'),
]

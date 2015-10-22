"""url configuration for the group_messaging application"""
from django.conf.urls import url
from group_messaging import views

urlpatterns = [
    url(r'^threads/$', views.ThreadsList().as_view(), name='get_threads'),
    url(r'^threads/(?P<thread_id>\d+)/$', views.ThreadDetails().as_view(), name='thread_details'),
    url(r'^threads/(?P<thread_id>\d+)/delete/$', views.DeleteOrRestoreThread('delete').as_view(),
        name='delete_thread'),
    url(r'^threads/(?P<thread_id>\d+)/restore/$', views.DeleteOrRestoreThread('restore').as_view(),
        name='restore_thread'),
    url(r'^threads/create/$', views.NewThread().as_view(), name='create_thread'),
    url(r'^senders/$', views.SendersList().as_view(), name='get_senders'),
    url(r'^post-reply/$', views.PostReply().as_view(), name='post_reply'),
]


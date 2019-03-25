from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from user.views import activate, Index, SignUp, LogIn, LogOut, ChangePassword


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^signup/$', SignUp.as_view(), name='signup'),
    url(r'^login/', LogIn.as_view(), name='login'),
    url(r'^logout/$', LogOut.as_view(), name='logout'),
    url(r'^password/$', ChangePassword.as_view(), name='change_password'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

]

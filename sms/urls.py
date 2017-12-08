"""sms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login),
    url(r'^home/$', views.home),
    url(r'^showStudents/$', views.showStudents),
    url(r'^showBanJis/$', views.showBanJis),
    url(r'^addStudent/$', views.addStudent),
    url(r'^addBanJi/$', views.addBanJi),
    url(r'^noAuthority/$', views.noAuthority),
    url(r'^delStudent/$', views.deleteStudent),
    url(r'^delTeacher/$', views.delTeacher),
    url(r'^delBanJi/$', views.delBanJi),
    url(r'^editStudent/$', views.editStudent),
    url(r'^editTeacher/$', views.editTeacher),
    url(r'^editBanJi/$', views.editBanJi),
    url(r'^studentInfo/$', views.studentInfo),
    url(r'^teacherInfo/$', views.teacherInfo),
    url(r'^banJiInfo/$', views.banJiInfo),
    url(r'^showTeachers/$', views.showTeachers),
    url(r'^addTeacher/$', views.addTeacher),
]

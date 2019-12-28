"""Mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from users.views import IndexView
import xadmin #导入xadmin
from django.views.generic import TemplateView#采用视图模板

from django.views.static import serve
from Mxonline.settings import MEDIA_ROOT,STATIC_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),#将默认admin改为xadmin
    url(r'^$', IndexView.as_view(),name="index"),#采用视图模板，其他应用的views采用类视图
    url(r'^users/', include('users.urls',namespace='users',app_name='users')),
    url(r'^organization/', include('organization.urls', namespace='organization', app_name='organization')),
    url(r'^courses/', include('courses.urls', namespace='courses', app_name='courses')),
    url(r'^captcha/', include('captcha.urls')),#注册模块验证码，要进行数据迁移生成验证码的表
    url(r'^media/(?P<path>.*)$',  serve, {"document_root":MEDIA_ROOT}),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
   # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    #url(r'^static/(?P<path>.*)$',  serve, {"document_root":STATIC_ROOT}),

]


#全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'

    #配置上传文件的处理
    #from django.views.static import serve
    #from Mxonline.settings import MEDIA_ROOT
    #url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),

    #from django.conf import settings
    #from django.conf.urls.static import static
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    #from django.contrib import admin
    # url(r'^admin/', admin.site.urls),
    # url(r'^login/$', TemplateView.as_view(template_name="login.html"),name="login"),
    #url(r'^courses/', include('courses.urls', namespace='courses', app_name='courses')),
    # url(r'^operation/', include('operation.urls', namespace='operation', app_name='operation')),






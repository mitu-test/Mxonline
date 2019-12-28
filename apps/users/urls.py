from django.conf.urls import url
from .views import LoginView,LogoutView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView
from .views import UserinfoView,UploadImageView,UpdatePwdView,SendEmailCodeView,UpdateEmailView,MyCourseView
from .views import MyFavOrgView,MyFavTeacherView,MyFavCourseView,MymessageView
urlpatterns = [

    url(r'^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    url(r'^info/$', UserinfoView.as_view(), name="user_info"),
    url(r'^image_upload/$', UploadImageView.as_view(), name="image_upload"),
    url(r'^update_pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),
    url(r'^mymessage/$', MymessageView.as_view(), name="mymessage"),


]
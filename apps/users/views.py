import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from django.contrib.auth.hashers import make_password #明文加密
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import UserProfile,EmailVerifyRecord,Banner
from courses.models import CourseOrg,Course
from organization.models import Teacher
from operation.models import UserCourse,UserFavorite,UserMessage


# Create your views here.

class IndexView(View):
    """
    主页视图
    """
    def get(self, request):
        # 轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 轮播课程
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        # 课程机构
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


class LoginView(View):
    """
    用户登录视图
    需在头部引入django认证和登录模块,以及登录后跳转到主页的HttpResponseRedirect和reverse模块
    from django.contrib.auth import authenticate, login
    from django.http import HttpResponseRedirect
    from django.core.urlresolvers import reverse
    类视图需要导入view模块from django.views.generic.base import View
    """
    def get(self,request):
        return render(request,"users/login.html",{})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 成功返回user对象,失败None
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                # 用户是否激活
                if user.is_active:
                    #登录
                    login(request, user)
                    #跳转到主页
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "users/login.html", {"msg": "用户未激活！"})
            else:
                return render(request,"users/login.html",{"msg":"用户名或密码错误！"})
        else:
            return render(request, "users/login.html",{"login_form":login_form})


class LogoutView(View):
    """
    退出账号视图
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class CustomBackend(ModelBackend):
    """
    增加邮箱登录
    用户可以通过邮箱或者用户名都可以登录
    用自定义authenticate方法，这里是继承ModelBackend类来做的验证，基础ModelBackend类，有authenticate方法
    需在头部导入from django.contrib.auth.backends import ModelBackend
    from django.db.models import Q
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    """
    用户注册
    """
    def get(self,request):
        register_form = RegisterForm()
        return render(request,"users/register.html",{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            # 如果用户已存在，则提示错误信息
            if UserProfile.objects.filter(email=user_name):
                return render(request, "users/register.html", {'register_form':register_form,'msg': "用户已注册，请直接登录！"})

            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对保存到数据库的密码加密，需要导入from django.contrib.auth.hashers import make_password
            user_profile.password = make_password(pass_word)
            user_profile.save()

            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册暮学在线网"
            user_message.save()

            send_register_email(user_name,"register")
            return render(request, "users/login.html")
        else:
            return render(request, "users/register.html", {'register_form': register_form})


class ActiveUserView(View):
    """
    用户激活
    """
    def get(self,request,active_code):
        # 查询邮箱验证码是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, "users/login.html")
        else:
            return render(request,"users/active_fail.html")


class ForgetPwdView(View):
    """
    忘记密码
    """
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,"users/forgetpwd.html",{"forget_form":forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email,"forget")
            return render(request,"users/send_success.html")
        else:
            return render(request,"users/forgetpwd.html",{"forget_form": forget_form})


class ResetView(View):
    """
    密码重置
    """
    def get(self,request,reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "users/password_reset.html", {"email": email})
        else:
            return render(request,"users/active_fail.html")


class ModifyPwdView(View):
    """
    修改密码视图
    """
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            email = request.POST.get("email","")
            if pwd1 != pwd2:
                return render(request, "users/password_reset.html", {"email": email,"msg":"前后密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "users/login.html")
        else:
            email = request.POST.get("email","")
            return render(request, "users/password_reset.html", {"email": email, "modify_form":modify_form })


class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """

    def get(self, request):
        return render(request,'users/usercenter-info.html',{})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
     用户图像修改
    """
    def post(self, request):
        # 上传的文件都在request.FILES里面获取，所以这里要多传一个这个参数
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱修改验证码
    """

    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, "update_email")

        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改邮箱
    """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'users/usercenter-mycourse.html', {
            "user_courses":user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我收藏的课程机构
    """

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象
        for fav_org in fav_orgs:
            # 取出fav_id也就是机构的id。
            org_id = fav_org.fav_id
            # 获取这个机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'users/usercenter-fav-org.html', {
            "org_list":org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
     我收藏的授课讲师
    """
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'users/usercenter-fav-teacher.html', {
            "teacher_list":teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的课程
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            teacher = Course.objects.get(id=course_id)
            course_list.append(teacher)
        return render(request, 'users/usercenter-fav-course.html', {
            "course_list":course_list,
        })


class MymessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        #对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)
        return render(request, 'users/usercenter-message.html', {
            "messages":messages
        })


def page_not_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    #全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response













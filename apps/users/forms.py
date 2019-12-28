from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    """
    登录表单验证
    """
    # 用户名密码不能为空
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=8)


class RegisterForm(forms.Form):
    """
    注册验证表单
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8)
    # 验证码，字段里面可以自定义错误提示信息
    captcha = CaptchaField(error_messages={"invalid":"验证码错误!"})


class ForgetForm(forms.Form):
    """
    忘记密码验证表单
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误!"})


class ModifyPwdForm(forms.Form):
    """
    重置密码
    """
    password1 = forms.CharField(required=True, min_length=8)
    password2 = forms.CharField(required=True, min_length=8)


class UploadImageForm(forms.ModelForm):
    # 用户图像上传
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']
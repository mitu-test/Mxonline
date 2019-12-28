from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser,User #引入默认user字段

# Create your models here.


class UserProfile(AbstractUser):
    """
    用户信息,继承自AbstractUser类，拓展User类
    image字段需要安装pillow
    需要在setting中重载AUTH_USER_MODEL = 'users.UserProfile'
    """
    nick_name = models.CharField(max_length=50,verbose_name="昵称",default="")
    birthday = models.DateField(verbose_name="生日",null=True,blank=True)
    gender = models.CharField(choices=(("male","男"),("female","女")),default="female",max_length=7)
    address = models.CharField(max_length=100,default="")
    mobile = models.CharField(max_length=11,null=True,blank=True)
    image = models.ImageField(upload_to="image/%Y/%m",verbose_name="用户图像",default="image/default.png",max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id,has_read=False).count()


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码
    DateTimeField字段需要导入from datetime import datetime
    """
    code = models.CharField(max_length=20,verbose_name="验证码")
    email = models.EmailField(max_length=50,verbose_name="邮箱")
    send_type = models.CharField(choices=(("register","注册"),("forget","找回密码"),("update_email","修改邮箱")),max_length=20)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}{1}'.format(self.code,self.email)


class Banner(models.Model):
    """
    首页轮播图
    image表示上传到哪里
    url表示点击图片的路径
    index表示控制轮播图的播放顺序
    """
    title = models.CharField(max_length=100,verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m",verbose_name="轮播图")
    url = models.URLField(max_length=200,verbose_name="访问地址")
    index = models.IntegerField(default=100,verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name
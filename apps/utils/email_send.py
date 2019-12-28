from random import Random
from django.core.mail import send_mail#django邮件发送模块

from users.models import EmailVerifyRecord
from Mxonline.settings import EMAIL_FROM


def random_str(randomlength=8):
    """
    生成随机字符串
    """
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        # 字符串实质上为一个列表，random.randint(0,length)随机生成一个列表下标
        str+=chars[random.randint(0,length)]
    return str


def send_register_email(email,send_type="register"):
    """
    发送注册邮件
    """
    # 发送之前先保存到数据库，到时候查询链接是否存在
    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        #通过上述random_str生成随机的code放入链接
        code = random_str(16)

    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == "register":
        # 定义邮件内容:
        email_title = "慕学在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/users/active/{0}".format(code)#format格式化输出
        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        # 如果发送成功
        if send_status:
            pass

    elif send_type == "forget":
        email_title = "慕学在线网注册密码重置链接"
        email_body = "请点击下面的链接重置密码：http://127.0.0.1:8000/users/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == "update_email":
        email_title = "慕学在线邮箱修改验证码"
        email_body = "你的邮箱验证码为：{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass







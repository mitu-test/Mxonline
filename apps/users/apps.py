from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    在xadmin中，使用户模型显示为中文
    还要在当前app中的，_init__.py文件中添加default_app_config = ""users.apps.UsersConfig""
    """
    name = 'users'
    verbose_name = "用户信息"


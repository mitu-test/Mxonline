from django.apps import AppConfig


class OperationConfig(AppConfig):
    """
    在xadmin中，使用户操作模型显示为中文
    还要在当前app中的，_init__.py文件中添加default_app_config = "operation.apps.OperationConfig"
    """
    name = 'operation'
    verbose_name = "用户操作"

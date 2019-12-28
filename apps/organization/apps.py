from django.apps import AppConfig


class OrganizationConfig(AppConfig):
    """
    在xadmin中，使机构模型显示为中文
    还要在当前app中的，_init__.py文件中添加default_app_config = ""organization.apps.OrganizationConfig""
    """
    name = 'organization'
    verbose_name = "机构管理"

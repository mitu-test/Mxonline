from django.apps import AppConfig


class CoursesConfig(AppConfig):
    """
    在xadmin中，使课程模型显示为中文
    还要在当前app中的，_init__.py文件中添加default_app_config = "courses.apps.CoursesConfig"
    """
    name = 'courses'
    verbose_name = "课程管理"

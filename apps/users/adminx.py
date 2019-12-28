import xadmin
from xadmin import views#创建xadmin的最基本管理器配置，并与view绑定
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row

from .models import EmailVerifyRecord,Banner


class UserProfileAdmin(UserAdmin):
    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()


class BaseSetting(object):
    """
    开启xadmin主题功能
    """
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    """
    在users app创建全局修改
    修改xadmin中的导航栏公司名称以及页面底部名称
    """
    # 修改title
    site_title = "慕学后台管理系统"
    # 修改footer
    site_footer = "慕学在线网"
    # 收起菜单
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    """
    xadmin中这里是继承object，不再是继承admin
    """
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-address-book-o'


class BannerAdmin(object):
    """
    主页轮播图
    """
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

#将xadmin基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView,BaseSetting)
# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView,GlobalSettings)



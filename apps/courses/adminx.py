import xadmin

from .models import Course, Lesson, Video, CourseResource,BannerCourse

#目前在添加课程的时候没法添加章节和课程资源，我们可以用inlines去实现这一功能，在课程后台显示章节和课程资源页面
class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


#在CourseAdmin中使用inlines添加上面两个的方法
class CourseAdmin(object):
    """
    课程信息
    """
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students','get_zj_nums','go_to']#直接使用函数名作为字段显示
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    ordering = ['-click_nums']#排序
    readonly_fields = ['click_nums']#只读字段，不能编辑
    list_editable = ['degree','desc']#在列表页可以直接编辑的字段
    exclude = ['fav_nums'] #不显示的字段
    inlines = [LessonInline,CourseResourceInline]#增加章节和课程资源
    refresh_times = [3,5]
    style_fields = {"detail":"ueditor"}#detail就是要显示为富文本的字段名
    import_excel = True

    # 重载queryset方法，来过滤出我们想要的数据的
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        # 只显示is_banner=True的课程
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        # obj实际是一个course对象
        obj = self.new_obj
        # 如果这里不保存，新增课程，统计的课程数会少一个
        obj.save()
        # 确定课程的课程机构存在。
        if obj.course_org is not None:
            # 找到添加的课程的课程机构
            course_org = obj.course_org
            # 课程机构的课程数量等于添加课程后的数量
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    """
    轮播课程
    """
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline,CourseResourceInline]

    # 重载queryset方法，来过滤出我们想要的数据的
    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        # 只显示is_banner=True的课程
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    """
    课程章节
    """
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']#xadmin外键使用方法


class VideoAdmin(object):
    """
    章节视频
    """
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    """
    课程资源
    """
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course,CourseResource,Video
from operation.models import UserFavorite,CourseComments,UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    """
    课程列表功能
    """
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time")
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]
        # 搜索功能
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            # icontains是包含的意思（不区分大小写）
            # Q可以实现多个字段，之间是or的关系
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))
        #排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3,request=request)
        courses = p.page(page)

        return render(request,'courses/course-list.html',{
            'all_courses':courses,
            'sort':sort,
            'hot_courses':hot_courses,
        })


class CourseDetailView(View):
    """
    课程详情
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        # 课程的点击数加1
        course.click_nums +=1
        course.save()
        #课程和机构初始状态为未收藏
        has_fav_course = False
        has_fav_org = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):
                has_fav_org = True
        # 课程标签
        # 通过当前标签，查找数据库中的课程
        tag = course.tag
        if tag:
            # 需要从1开始不然会推荐自己
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request,'courses/course-detail.html',{
            'course':course,
            'relate_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin,View):
    """
     课程章节信息
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户是否已经学习了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        # 如果没有学习该门课程就关联起来
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 找到学习这门课的所有用户
        user_cousers = UserCourse.objects.filter(course=course)
        # 找到学习这门课的所有用户的id
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        # 通过所有用户的id,找到所有用户学习过的所有过程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        # 通过所有课程的id,找到所有的课程，按点击量去五个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        # 资源
        all_resources = CourseResource.objects.filter(course=course)
        return render(request,'courses/course-video.html',{
            'course':course,
            'all_resources':all_resources,
            'relate_courses':relate_courses,
        })


class VideoPlayView(View):
    """
    视频播放页面
    """
    def get(self,request,video_id):
        video = Video.objects.get(id=int(video_id))
        # 通过外键找到章节再找到视频对应的课程
        course = video.lesson.course

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_cousers = UserCourse.objects.filter(course=course)
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request,'courses/course-play.html',{
            'course':course,
            'all_resources':all_resources,
            'relate_courses':relate_courses,
            'video':video,
        })


class CommentsView(LoginRequiredMixin,View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_cousers = UserCourse.objects.filter(course=course)
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        all_comments =  CourseComments.objects.all()
        return render(request,'courses/course-comment.html',{
            'course': course,
            'all_resources': all_resources,
            'all_comments':all_comments,
            'relate_courses': relate_courses,

        })


class AddCommentsView(View):
    """
    添加评论
    """
    def post(self,request):
        # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id",0)
        comments = request.POST.get("comments","")
        if int(course_id) >0 and comments:
            # 实例化一个course_comments对象
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            # 分别把评论的课程、评论的内容和评论的用户保存到数据库
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')





from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg,CityDict,Teacher
from operation.models import UserFavorite
from .forms import UserAskForm
from courses.models import Course

# Create your views here.


class OrgView(View):
    """
    课程机构视图
    """
    def get(self,request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 机构搜索功能
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) |
                                       Q(desc__icontains=search_keywords))

        #城市筛选
        city_id = request.GET.get('city', "")#为一个字符串
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 机构数量
        org_nums = all_orgs.count()

        #排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取1个出来，每页显示1个
        p = Paginator(all_orgs, 1,request=request)
        orgs = p.page(page)
        return render(request,"organization/org_list.html",{
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort,

        })


class AddUserAskView(View):
    """添加用户咨询"""
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # 如果保存成功,返回json字符串,后面content type是告诉浏览器返回的数据类型
            user_ask = userask_form.save(commit=True)#commit为True立即保存数据库
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
            return HttpResponse('{"status":"fail","msg":"咨询出错！"}',content_type='application/json')


class OrgHomeView(View):
    """机构首页"""
    def get(self,request,org_id):
        current_page = "home"
        # 根据id找到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        #收藏类型
        fav_num = 2
        # 默认未收藏状态
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                #数据存在时就显示收藏状态
                has_fav = True
        # 反向查询到课程机构的所有课程和老师
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,'organization/org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav': has_fav,
            'fav_num':fav_num,

        })


class OrgCourseView(View):
    """
    机构课程
    """
    def get(self,request,org_id):
        current_page = "course"
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        #收藏类型
        fav_num = 1
        # 默认未收藏状态
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=1):
                has_fav = True
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()
        return render(request,'organization/org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
            'fav_num': fav_num,
        })


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self,request,org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 收藏类型
        fav_num = 2
        # 默认未收藏状态
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'organization/org-detail-desc.html',{
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
            'fav_num': fav_num,

        })


class OrgTeacherView(View):
    """
    机构教师
    """
    def get(self,request,org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        #收藏类型
        fav_num = 3
        #默认未收藏状态
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=3):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request,'organization/org-detail-teachers.html',{
            'all_teachers': all_teachers,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
            'fav_num': fav_num,
        })


class AddFavView(View):
    """
    用户收藏和取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)
        # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')

        else:
            # 如果记录不存在，表示用户添加收藏
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    """
    讲师列表
    """
    def get(self,request):
        all_teachers = Teacher.objects.all()
        # 总共有多少老师使用count进行统计
        teacher_nums = all_teachers.count()

        # 搜索功能
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                               Q(work_company__icontains=search_keywords) |
                                               Q(work_position__icontains=search_keywords))
        # 人气排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")
        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]
        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 1,request=request)
        teachers = p.page(page)

        return render(request,'organization/teachers-list.html',{
            "all_teachers":teachers,
            "sorted_teacher":sorted_teacher,
            "sort":sort,
            "teacher_nums":teacher_nums,
        })


class TeacherDetailView(View):
    # 讲师详情
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)
        # 教师收藏和机构收藏
        has_teacher_faved = False
        has_org_faved = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id,fav_type=3):
                has_teacher_faved = True

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id,fav_type=2):
                has_org_faved = True
        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]
        return render(request,'organization/teacher-detail.html',{
            "teacher":teacher,
            "all_courses":all_courses,
            "sorted_teacher":sorted_teacher,
            "has_teacher_faved":has_teacher_faved,
            "has_org_faved":has_org_faved,


        })
















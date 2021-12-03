import re
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.
from django.views import View
from django.db import DatabaseError
from users.models import User
from django.contrib.auth import logout
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from home.models import ArticleCategory, Article


# 定义注册视图


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        #  接收请求参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')

        # 验证参数
        if not all([username, password, password2, mobile]):
            return HttpResponseBadRequest('缺少字段')
        if not re.match(r'^[a-zA-Z0-9_-]{3,20}$', username):
            return HttpResponseBadRequest('请输入2-20位字符的用户名')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseBadRequest('请输入8-20位密码，密码是数字，字母')
        if password != password2:
            return HttpResponseBadRequest('两次密码不一致')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('请输入正确的手机号码')

        try:
            user = User.objects.create_user(username=username,
                                            mobile=mobile,
                                            password=password)
        except DatabaseError:

            return HttpResponseBadRequest('注册失败')

        from django.contrib.auth import login
        login(request, user)
        response = redirect(reverse('home:index'))
        response.set_cookie('is_login', True)
        response.set_cookie('username', user.username, max_age=7 * 24 * 3600)
        return response


# 定义登录视图

class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remake = request.POST.get('remake')
        if not re.match(r'^[a-zA-Z0-9_-]{3,20}$', username):
            return HttpResponseBadRequest('请输入正确的用户名')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseBadRequest('请输入8-20位密码，密码是数字，字母')

        from django.contrib.auth import authenticate

        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponseBadRequest('用户名或者密码错误')

        #  状态保持

        from django.contrib.auth import login
        login(request, user)
        response = redirect(reverse('home:index'))
        if remake != 'on':
            request.session.set_expiry(0)
            response.set_cookie('is_login', True)
            response.set_cookie('username', user.username, max_age=14 * 24 * 3600)
        else:
            request.session.set_expiry(None)
            response.set_cookie('is_login', True)
            response.set_cookie('username', user.username, max_age=14 * 24 * 3600)

        return response


# 注销登录视图

class LogoutView(View):

    def get(self, request):
        logout(request)
        response = redirect(reverse('home:index'))
        response.delete_cookie('username')
        return response


# 个人中心视图

class UserView(View):

    def get(self, request):
        user = request.user
        categories = ArticleCategory.objects.all()
        cat_id = request.GET.get('cat_id', 1)
        try:
            category = ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('没有此分类')
        context = {
            'username': user.username,
            'mobile': user.mobile,
            'user_desc': user.user_desc,
            'id': user.id,
            'categories': categories,
            'category': category
        }
        return render(request, 'user.html', context=context)

    def post(self, request):
        user = request.user
        username = request.POST.get('username', user.username)
        user_desc = request.POST.get('user_desc', user.user_desc)
        mobile = request.POST.get('mobile', user.mobile)

        try:
            user.username = username
            user.user_desc = user_desc
            user.mobile = mobile
            user.save()
        except Exception:

            return HttpResponseBadRequest('修改失败，请稍后再试')
        response = redirect(reverse('users:user'))
        response.set_cookie('username', user.username, max_age=14 * 24 * 3600)
        return response


#  博客发布视图
class WriteView(View):

    def get(self, request):
        categories = ArticleCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'write.html', context)

    def post(self, request):
        title = request.POST.get('title')
        category_id = request.POST.get('category_id')
        sumary = request.POST.get('sumary')
        tags = request.POST.get('tags')
        content = request.POST.get('content')
        user = request.user
        if not all([title, user, tags, sumary, category_id, content]):
            return HttpResponseBadRequest('参数不全')
        try:
            category = ArticleCategory.objects.get(id=category_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseBadRequest('没有此分类')
        try:
            article = Article.objects.create(
                title=title,
                author=user,
                tags=tags,
                category_id=category_id,
                sumary=sumary,
                content=content,
            )
        except Exception:
            return HttpResponseBadRequest('发布失败，请稍后再试')
        path = reverse('home:article')+'?id={}'.format(article.id)
        return redirect(path)

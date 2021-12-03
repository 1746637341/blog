from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpResponseNotFound
from home.models import ArticleCategory, Article, Comment

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage


# Create your views here.

# 定义主页不同类别内容视图

class IndexView(View):
    def get(self, request):
        categories = ArticleCategory.objects.all()
        cat_id = request.GET.get('cat_id', 1)
        try:
            category = ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('没有此分类')

        articles = Article.objects.filter(category=category)  # 获得所有文章
        #  推荐文章排序，根据阅读量 显示10条
        hot_article = Article.objects.order_by('-total_views')[:10]
        context = {
            'categories': categories,
            'category': category,
            'articles': articles,
            'cat_id': cat_id,
            'hot_article': hot_article,
        }
        return render(request, 'index.html', context=context)



# 定义主页展示视图
#
# class IndexAllView(View):
#     def get(self, request):
#         categories = ArticleCategory.objects.all()
#         cat_id = request.GET.get('cat_id')
#         category = ArticleCategory.objects.get(id=cat_id)
#         article = Article.objects.all()
#         context = {
#             'article': article,
#             'categories': categories,
#             'category': category,
#             'cat_id': cat_id
#         }
#         return render(request, 'index.html', context=context)

# 定义文章详情页面视图
class ArticleView(View):
    def get(self, request):
        id = request.GET.get('id')
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            pass
        else:
            article.total_views += 1
            article.save()
        categories = ArticleCategory.objects.all()
        hot_article = Article.objects.order_by('-total_views')[:9]
        page_size = request.GET.get('page_size', 10)
        page_num = request.GET.get('page_num', 1)
        comments = Comment.objects.filter(article=article).order_by('-created')
        total_count = comments.count()
        from django.core.paginator import Paginator, EmptyPage
        paginator = Paginator(comments, page_size)
        try:
            page_comments = paginator.page(page_num)
        except EmptyPage:
            return HttpResponseNotFound('empty page')

        total_page = paginator.num_pages

        context = {
            'categories': categories,
            'category': article.category,
            'article': article,
            'hot_article': hot_article,
            'total_count': total_count,
            'comments': comments,
            'page_size': page_size,
            'total_page': total_page,
            'page_num': page_num
        }
        return render(request, 'article.html', context=context)

    #  发表评论
    def post(self, request):
        user = request.user
        # 判断用户是否已经登录
        if user and user.is_authenticated:
            id = request.POST.get('id')
            content = request.POST.get('content')
            try:
                article = Article.objects.get(id=id)
            except Article.DoesNotExist:
                return HttpResponseNotFound('没有此文章')
            Comment.objects.create(
                content=content,
                article=article,
                user=user
            )
            # 修改评论数
            article.comments_count += 1
            article.save()
            path = reverse('home:article') + '?id={}'.format(article.id)
            return redirect(path)
        else:
            return redirect(reverse('users:login'))
# class BaseView(View):
#     def get(self, request):
#         categories = ArticleCategory.objects.all()
#         cat_id = request.GET.get('cat_id', 1)
#         try:
#             category = ArticleCategory.objects.get(id=cat_id)
#         except ArticleCategory.DoesNotExist:
#             return HttpResponseNotFound('没有此分类')
#         context = {
#             'categories': categories,
#             'category': category,
#             'cat_id': cat_id,
#         }
#         return render(request, 'index.html', context=context)

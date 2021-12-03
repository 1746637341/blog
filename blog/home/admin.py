from django.contrib import admin
from .models import ArticleCategory
from .models import Article
from .models import Comment
# Register your models here.
# 注册ArticleCategory模型
admin.site.register(ArticleCategory)
admin.site.register(Article)
admin.site.register(Comment)

#  进行home子应用的视图路由

from django.urls import path, re_path
from home.views import IndexView, ArticleView

# from home.views import IndexAllView

urlpatterns = [

    #     re_path(r'^cat_id(\d)$', IndexView.as_view(), name='index'),
    #     re_path(r'^$', IndexAllView.as_view(), name='index_all'),
    path('', IndexView.as_view(), name='index'),
    path('article/', ArticleView.as_view(), name='article'),
]

# 进行users子应用的视图路由

from django.urls import path
from users.views import RegisterView
from users.views import LoginView
from users.views import LogoutView
from users.views import UserView
from users.views import WriteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # 注册路由
    path('login/', LoginView.as_view(), name='login'),  # 登录路由
    path('logout/', LogoutView.as_view(), name='logout'),  # 注销登录路由
    path('user/', UserView.as_view(), name='user'),  # 个人中心路由
    path('write/', WriteView.as_view(), name='write'),  # 编写博客路由
]

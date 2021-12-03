from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    # 添加手机号字段
    mobile = models.CharField(max_length=11, unique=True, blank=False)
    # 添加头像字段
    avatar = models.ImageField(upload_to='avatar/%Y%m%d', blank=True)
    # 添加简介信息字段
    user_desc = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = 'tb_users'  # 修改默认user表名
        verbose_name = '用户管理'  # admin后台显示
        verbose_name_plural = verbose_name  # admin后台显示

    def __str__(self):
        return self.mobile

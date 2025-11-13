from django.db import models
from django.contrib.auth.models import AbstractUser  #导入抽象用户类


class User(AbstractUser):
    """自定义用户模型"""
    email = models.EmailField(verbose_name="邮箱",unique=True)
    phone = models.CharField(max_length=20,verbose_name="手机号",null=True,blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'

        #下面两个是配合完成的
        verbose_name = "用户"
        verbose_name_plural = verbose_name









#个人信息表
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """用户详细信息表"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='关联用户'
    )
    school = models.CharField(max_length=100, verbose_name="毕业院校", blank=True, null=True)
    major = models.CharField(max_length=100, verbose_name="学习专业", blank=True, null=True)
    expected_job = models.CharField(max_length=100, verbose_name="期望岗位", blank=True, null=True)
    expected_salary = models.CharField(max_length=50, verbose_name="期望薪资", blank=True, null=True)
    expected_city = models.CharField(max_length=50, verbose_name="期望城市", blank=True, null=True)
    current_address = models.CharField(max_length=200, verbose_name="当前住址", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"{self.user.username} 的个人信息"

    class Meta:
        db_table = 'user_profiles'
        verbose_name = '用户详细信息'
        verbose_name_plural = verbose_name


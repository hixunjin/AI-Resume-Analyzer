from django.contrib.auth import get_user_model   #用户模型工具
from django.contrib.auth.password_validation import validate_password  #Django密码校验函数
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


#获取当前使用的用户模型
User = get_user_model()


#注册模型序列化器---相当于是请求模型
class UserRegisterSerializer(serializers.ModelSerializer):
    """
       用于注册新用户的序列化器：
       - 检查两次输入的密码是否一致
       - 验证密码强度（使用 Django 的密码验证规则）
       - 创建用户时自动加密密码
    """
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)

    #绑定模型，写出要序列化的模型字段
    class Meta:
        model = User
        fields = ('username','email','password','password2')


    #验证两次密码是否一致
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':'两次密码输入不一致'})
        return attrs


    #防止邮箱重复注册
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已经被注册！')
        return value


    #创建数据函数
    def create(self, validated_data):
        """
                创建用户对象时：
                - 删除 password2（数据库里没有这个字段）
                - 使用 create_user() 自动加密密码并保存
        """
        validated_data.pop('password2')   #移除重复字段
        user = User.objects.create_user(**validated_data)
        return user



#用户响应模型
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('id','username','email','date_joined')   #返回的字段





#基于JWT登录的自定义序列化器
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """自定义登录序列化器，支持角色判断"""

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # 检查是否激活
        if not user.is_active:
            raise serializers.ValidationError("账号未激活，请联系管理员。")

        # 登录成功后返回额外的用户信息
        data.update({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        })

        return data


#用户详细信息校验模型



from rest_framework import serializers
from apps.users.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """用户详细信息序列化器"""

    # 可选：显示用户名而不是ID
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'school', 'major', 'expected_job',
            'expected_salary', 'expected_city', 'current_address',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_expected_salary(self, value):
        """可选校验示例"""
        if value and not any(char.isdigit() for char in value):
            raise serializers.ValidationError("薪资应包含数字，例如 '15K-20K'")
        return value





#用户信息，对两个数据模型进行数据校验
from rest_framework import serializers



class UserFullInfoSerializer(serializers.Serializer):
    """组合序列化器：包含用户基本信息 + 详细信息"""
    user = UserSerializer()
    profile = UserProfileSerializer()






from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'confirm_password']

    def validate_email(self, value):
        """邮箱唯一校验"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被注册。")
        return value

    def validate(self, data):
        """两次密码一致性校验"""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("两次输入的密码不一致。")
        return data

    def create(self, validated_data):
        """创建用户并加密密码"""
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

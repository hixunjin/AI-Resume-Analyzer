from rest_framework.decorators import api_view,permission_classes
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from apps.resumes.models import Resume
from apps.resumes.serializers import ResumeSerializer

#登录接口
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer


from .serializers import UserProfileSerializer,UserFullInfoSerializer
from .models import UserProfile




#注册视图类
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={201: '注册成功', 400: '请求错误'},
        operation_summary="用户注册接口",
        operation_description="注册新用户（输入用户名、邮箱和两次密码）"
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return Response({'message':'注册成功','user':user_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





#获取当前用户信息，这个用于个人信息
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):

    #创建校验类，通过校验类将数据从数据从返回出去，校验类指定了校验以及要返回的字段
    serializer = UserSerializer(request.user)

    #返回数据
    return Response(serializer.data)





#调用自定义JWT登录序列化器
class MyTokenObtainPairView(TokenObtainPairView):
    """自定义 JWT 登录接口"""

    #自定义校验器：检查是否激活，返回额外信息
    serializer_class = MyTokenObtainPairSerializer



class LogoutView(APIView):
    """
    注销用户（黑名单 JWT）
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 获取 JWT refresh token
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            # 将 token 加入黑名单
            token.blacklist()
            return Response({'message': '注销成功'}, status=200)
        except Exception as e:
            return Response({'error': '无效的 token'}, status=400)




#用户详情请信息的 增加、修改
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="获取当前用户的个人信息",
        responses={200: UserProfileSerializer()},
    )
    def get(self,request):
        try:
            #尝试通过一对一获取用户对应的详细信息
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return Response({'detail':'个人信息未创建'},status=status.HTTP_400_BAD_REQUEST)


        #组织数据
        serializer = UserProfileSerializer(profile)

        #返回数据，用户的当前详细信息
        return Response(serializer.data)


    #post请求，修改数据

    @swagger_auto_schema(
        operation_summary="更新当前用户的个人信息",
        request_body=UserProfileSerializer,  # ✅ 告诉 Swagger 使用这个序列化器渲染表单
        responses={200: UserProfileSerializer()},
    )
    def put(self,request):
        # 若不存在则自动创建
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






#获取用户的详细信息的获取
class UserFullInfoView(APIView):
    """返回用户基本信息 + 详细信息"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="获取当前登录用户的完整信息（User + Profile）",
        responses={200: UserFullInfoSerializer()},
    )
    def get(self, request):
        user = request.user
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = None  # 用户可能还没完善信息

        user_data = UserSerializer(user).data
        profile_data = UserProfileSerializer(profile).data if profile else {}

        # ✅ 取出该用户上传的最新简历
        resume = Resume.objects.filter(user=user).order_by('-created_at').first()
        resume_data = ResumeSerializer(resume).data if resume else None
        result = {
            "user": user_data,
            "profile": profile_data,
            'resume': resume_data,
        }

        return Response(result, status=status.HTTP_200_OK)



#注册视图类
class RegisterUserView(APIView):
    """用户注册接口"""

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "注册成功",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

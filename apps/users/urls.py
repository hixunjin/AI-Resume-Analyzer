from django.urls import path
from apps.users import views
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView



#路由
urlpatterns = [
    path('register/',views.RegisterView.as_view()),


    #JWT登录接口,调用自定义JWT登录接口(检查用户身份)
    path('login/',views.MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('refresh/',TokenRefreshView.as_view(),name='token_refresh'),




    #详细信息的添加
    path('api/profile/', views.UserProfileView.as_view(), name='user-profile'),


    #个人中心的信息获取接口
    path('profile/full/', views.UserFullInfoView.as_view(), name='user_full_info'),

    #注册地址
    path('register/', views.RegisterUserView.as_view(), name='user_register'),





    #退出登录（未使用的接口）
    path('logout/',views.LogoutView.as_view(),name='user-logout'),
]


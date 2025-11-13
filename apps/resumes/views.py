from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser
from .serializers import ResumeUploadSerializer
from celery_tasks.tasks import parse_resume_task
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.ai.tasks import analyze_resume_task
import os
from django.http import FileResponse, Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Resume

#视图函数形式:装饰器+函数，不是类


#简历上传和解析接口，关联简历上传用户，调用异步解析接口任务进行解析简历
@swagger_auto_schema(
    method='post',
    operation_summary="上传简历接口",

    #描述信息
    operation_description=(
        "功能：\n"
        "- 接收用户上传的 PDF / Word 简历\n"
        "- 保存到数据库\n"
        "- 异步调用 Celery 任务解析简历文本"
    ),
    #手动定义请求参数
    manual_parameters=[
        openapi.Parameter(
            name='file',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            description='上传的简历文件（支持 .pdf / .docx）',
            required=True,
        ),
    ],
    responses={201: "上传成功"},
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  #表示此接口需要进行登录
@parser_classes([MultiPartParser,FormParser])   #支持上传文件的解析器
def upload_resume(request):

    print("上传简历函数工作中！")
    """
        上传简历接口
        功能：
            - 接收用户上传的 PDF / Word 简历
            - 保存到数据库
            - 异步调用 Celery 任务解析简历文本
    """

    #创建校验模型对象,接收上传的简历
    serializer = ResumeUploadSerializer(data=request.data)

    #检查数据是否合法
    if serializer.is_valid():

        #保存简历对象，并关联当前登录用户
        #serializer已经携带了部分数据（校验类指定的字段数据）
        resume = serializer.save(user=request.user)

        #异步解析简历，即调用异步任务，异步任务调用简历解析函数获取长文本，然后将内容
        #存储到数据表的 content 字段
        #需要传递简历的id，以便对其操作


        #调用简历解析工具，解析出文本内容，存储到表字段 content
        parse_resume_task.delay(resume.id)     #这里已经将 text 保存到content字段中



        #调用AI进行分析简历(异步执行)，调用的时候，再去除表中的content，然后分析
        analyze_resume_task.delay(resume.id)




        #简历解析后，需要调用AI解析函数，对简历进行解析

        #成功后返回响应
        return Response({
            'message':'简历上传成功!',
            'resume_id':resume.id
        })






    #数据不合法
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




#获取用户上传的简历
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_resumes(request):
    """
        查看用户上传的所有简历接口
        功能：
            - 查询当前用户上传的所有简历
            - 按创建时间倒序返回
    """

    #查询出当前用户的简历，按照创建时间进行倒序排序
    resumes = Resume.objects.filter(user=request.user).order_by('-created_at')
    serializer = ResumeUploadSerializer(resumes,many=True)
    return Response(serializer.data)



#用户下载自己的简历







#下载路径和上传路径是一样的，下载时的文件就是上传的文件


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_resume(request, resume_id):

    print("工作中")
    """
    下载指定 resume_id 的简历文件
    """
    try:
        resume = Resume.objects.get(id=resume_id, user=request.user)
        print(11111111111111111111111111111)
        print(resume)
    except Resume.DoesNotExist:

        print(22222222)
        raise Http404("简历不存在")

    # 获取文件的相对路径，例如：resumes/简历_MUTBgeA.pdf
    resume_file_path = str(resume.file)

    # 获取 MEDIA_ROOT 的路径，这个路径是你保存文件的根目录

    # 拼接出完整的文件路径
    # 拼接出完整的文件路径
    B = r"C:\Users\86131\Desktop\Python后端\Django\项目实战\AI-Project\AI-Resume-Analyzer\AI_Resume_Analyzer\media"
    target_file = B +"\\"+ resume_file_path



    # 处理路径：去除 'media' 和替换所有斜杠为反斜杠
    target_file2 = target_file.replace('/', '\\')  # 替换所有斜杠为反斜杠


    print("处理结果111:"+target_file2)

    # 检查文件是否存在
    if not os.path.exists(target_file2):
        raise Http404("文件不存在")

    # 返回文件下载
    response = FileResponse(open(target_file2, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(target_file2)}"'
    return response








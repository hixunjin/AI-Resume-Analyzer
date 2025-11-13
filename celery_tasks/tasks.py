from celery import shared_task
from apps.resumes.models import Resume
from apps.resumes.utils import parse_pdf,parse_docx
from pathlib import Path


@shared_task
def parse_resume_task(resume_id):
    try:
        """获取简历对象"""
        resume = Resume.objects.get(id=resume_id)
        resume.status = 'processing'
        resume.save()

        # 获取简历路径和文件类型
        file_path = resume.file.path
        ext = Path(file_path).suffix.lower()

        # 判断文件类型，并调用对应文件类型的解析函数，将简历内容解析为长文本
        if ext == '.pdf':
            text = parse_pdf(file_path)
        elif ext in ['.doc', '.docx']:
            text = parse_docx(file_path)
        else:
            raise ValueError("不支持的文件格式")

        #将获取到的长文本存储到数据库，并更新解析状态为完成


        #content为空，检查下是否有内容
        print(1111111111111111111111111111)
        print("content内容:"+text)


        resume.content = text
        resume.status = "done"
        resume.save()

    #异常捕捉
    except Exception as e:
        resume.status = 'failed'
        resume.content = f"解析失败:{e}"
        resume.save()







from django.db import models
from django.conf import settings


class Resume(models.Model):
    """
    上传用户、简历文件、内容、上传时间、解析状态
    """

    #和模型 User 一对一关系，在上传简历的时候，会带上用户id
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="上传用户")

    #下面的字段应该在后台可以收到简历文件
    file = models.FileField(upload_to='resumes/',verbose_name="简历文件")

    content = models.TextField(blank=True,null=True,verbose_name="解析后的文本")
    created_at = models.DateTimeField(auto_now_add=True)

    #解析状态
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending','等待解析'),
            ('processing','解析中'),
            ('done','已经完成'),
            ('failed','解析失败')
        ],
        verbose_name="解析状态"
    )

    def __str__(self):
        return f"{self.user.username}-{self.file.name}"

    class Meta:
        db_table = 'resumes'
        verbose_name = '简历'
        verbose_name_plural = verbose_name


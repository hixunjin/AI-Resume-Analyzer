from django.db import models
from apps.resumes.models import Resume


class Report(models.Model):
    """AI 分析报告模型"""
    #这里是外键，和简历模型是一对一
    resume = models.OneToOneField(Resume,on_delete=models.CASCADE,related_name='report')

    score = models.FloatField(default=0,help_text='匹配度评分（0-100）')
    summary = models.TextField(blank=True,null=True,help_text='简历内容摘要')
    suggestions = models.TextField(blank=True,null=True,help_text='优化建议')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    def __str__(self):
        return f"Report for {self.resume.name}(Score:{self.score})"





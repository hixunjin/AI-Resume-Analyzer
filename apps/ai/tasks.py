from celery import shared_task
from apps.ai.services import analyze_resume_with_ai
from apps.report.models import Report
from apps.resumes.models import Resume
import re
import logging

logger = logging.getLogger(__name__)

@shared_task
def analyze_resume_task(resume_id):
    """异步执行简历AI分析任务"""
    try:
        # 1. 获取简历记录
        resume = Resume.objects.get(id=resume_id)
        resume.status = 'processing'
        resume.save()

        # 2. 调用 AI 分析函数
        ai_result = analyze_resume_with_ai(resume.content)

        logger.info(f"全部内容:{ai_result}")

        if not ai_result:
            raise ValueError("AI 分析结果为空")

        # 3. 从 AI 返回文本中解析关键信息（简单正则解析）
        score_match = re.search(r"得分[：:\s\*]*([0-9]+(?:\.[0-9]+)?)", ai_result)
        summary_match = re.search(r"摘要[:：]?\s*(.*?)(?=建议[:：]|$)", ai_result, re.S)
        suggestion_match = re.search(r"建议[:：]?\s*(.*)", ai_result, re.S)

        score = float(score_match.group(1)) if score_match else 0
        summary = summary_match.group(1).strip() if summary_match else ai_result[:200]
        suggestions = suggestion_match.group(1).strip() if suggestion_match else "暂无建议"

        # 4. 创建 Report 记录
        Report.objects.create(
            resume=resume,
            score=score,
            summary=summary,
            suggestions=suggestions
        )

        # 5. 更新 Resume 状态为完成
        resume.status = 'done'
        resume.save()

        logger.info(f"✅ 简历 {resume.id} 分析完成，得分：{score}")

    except Exception as e:
        logger.error(f"❌ 简历 {resume_id} 分析失败: {e}")

        resume = Resume.objects.filter(id=resume_id).first()
        if resume:
            resume.status = 'failed'
            resume.save()

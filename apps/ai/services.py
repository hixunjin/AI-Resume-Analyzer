#本初定义的函数，需要在 tasks中调用，完成异步支持
#调用AI模型分析简历
import os
from openai import OpenAI
from apps.ai.prompts import BASIC_PROMPT_TEMPLATE

# 初始化 DeepSeek 对象
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

def analyze_resume_with_ai(resume_text: str):
    """调用 DeepSeek AI 进行简历分析"""
    #使用提示词模板，并传入简历内容
    prompt = BASIC_PROMPT_TEMPLATE.format(resume_text=resume_text)

    #开始分析
    try:
        # 调用 DeepSeek 的 ChatCompletion 接口
        response = client.chat.completions.create(
            #Deepseek V3模型
            model="deepseek/deepseek-chat-v3-0324",

            messages=[
                {"role": "system", "content": "你是一个专业的人才分析助手"}, #系统角色：定义 AI 的身份
                {"role": "user", "content": prompt}    # 用户消息：简历分析的提示词
            ],
            temperature=0.7   # 控制生成内容的随机性，0.7 表示适中创造力
        )


        #获取分析结果，并取出首位空格
        result = response.choices[0].message.content.strip()
        return result

    #异常捕获
    except Exception as e:
        print(f"AI 调用失败: {e}")
        return None

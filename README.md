AI 简历分析平台（AI Resume Analyzer）项目规划文档

一、项目概述

项目名称：
AI 简历分析平台（AI Resume Analyzer）

这个项目的使用者，分为求职者和招聘者，后台管理，是供管理员查看统计数据的




项目简介：
该系统为求职者与招聘方提供智能化简历分析与岗位匹配服务。
用户可上传简历文件（PDF/Word），系统自动解析内容并调用 AI 模型进行分析，生成报告，指出简历亮点与改进建议，并评估与目标岗位的匹配度。
管理员可在后台查看统计报表（岗位热度、用户分析数据、AI调用情况等）。

目标人群：
求职者：希望获得简历优化建议与岗位匹配度
招聘企业：批量筛选候选人简历
面试展示：体现 Django + AI + 异步任务 + 可视化综合能力


二、项目核心功能模块
| 模块         | 功能说明                            |
| ---------- | ------------------------------- |
| 用户模块    | 注册登录、JWT 认证、个人中心                |
| 简历模块    | 简历上传、存储、解析、AI分析任务调度             |
| AI 分析模块 | 调用 DeepSeek 接口，生成简历评估报告 |
| 报告模块    | 展示简历分析报告、匹配度评分、优化建议             |
| 后台统计模块  | 管理员查看统计图表（调用量、岗位匹配度趋势）          |
| 系统管理员模块    | 日志管理、任务调度、系统设置（AI Key、速率限制）     |






三、技术栈



| 层级    | 技术                                    | 说明            |
| ----- | ------------------------------------- | ------------- |
| 后端框架  | Django 5.x                            | 主框架           |
| API 层 | Django REST Framework                 | 构建 RESTful 接口 |
| 异步任务  | Celery                              | 调度 AI 分析任务    |
| AI 接口 | DeepSeek                              | 调用模型生成简历分析报告  |
| 文件解析  | pdfminer.six / python-docx / docx2txt | 提取简历内容文本      |
| 数据库   |  MySQL                                 | 存储用户与简历记录     |
| 缓存    | Redis                                 | 存储任务状态、报告缓存   |
| 前端    | 静态HTML CSS  JS 修饰使用 Bootstrap框架链接        | 页面展示与数据可视化    |
| 部署    | Docker + Nginx + Gunicorn             | 容器化部署         |
| 安全    | JWT 认证 / 文件安全检测 / 限流机制                | 防止滥用与攻击       |


四、程序截图
1.注册和登录
![register](https://github.com/user-attachments/assets/4c2a767d-b69b-4a1d-929f-a47bca23b421)


![login](https://github.com/user-attachments/assets/d9b7a502-cc41-4662-8e56-287e4179e3ae)


2.首页

![index](https://github.com/user-attachments/assets/6b3716b0-4c39-403d-ba39-656613393102)


3.上传简历

![shangchuan](https://github.com/user-attachments/assets/d0e43834-3d3f-4b74-bbdc-54ea3547efa7)


4.查看与下载报告
![look_report](https://github.com/user-attachments/assets/7a39f381-52d1-48d0-8572-9f087b738098)


![download_report](https://github.com/user-attachments/assets/8ce33ec2-24cb-41b0-9000-625c5227c508)


5.个人中心

![user_info](https://github.com/user-attachments/assets/a5fc42d5-84f2-4212-95f5-55d85feb6a55)








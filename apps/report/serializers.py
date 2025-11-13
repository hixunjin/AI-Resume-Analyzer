from rest_framework import serializers
from apps.report.models import Report


#报告模型校验器，校验的字段为模型的全部字段
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
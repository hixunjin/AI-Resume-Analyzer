from rest_framework import serializers
from .models import Resume

#上传简历校验模型
#原理:根据数据模型中的字段类型进行校验请求字段是否合法
#校验类有接收、校验、存储数据的作用（serializer.save()）
#在保存数据的时候，如果校验类只对部分字段进行校验，那么save函数需要补充剩余的参数，这种需要
#补充的参数一般是 user
class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:

        #指定模型，以及模型校验字段
        model = Resume
        fields = ['id','file','status','created_at']

        #限制只读字段，防止用户非法修改系统自动生成的数据
        read_only_fields = ['id','status','created_at']




from rest_framework import serializers
from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    """简历序列化器"""

    # 只读字段：显示用户名
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Resume
        fields = [
            'id',
            'username',
            'file',
            'content',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'username', 'content', 'status', 'created_at']

    def create(self, validated_data):
        """
        上传简历时，自动关联当前登录用户
        """
        request = self.context.get('request')
        user = request.user if request else None
        resume = Resume.objects.create(user=user, **validated_data)
        return resume

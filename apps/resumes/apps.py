from django.apps import AppConfig


#和django项目不同等是，DRF需要在这里也注册下应用，不然无法识别到应用
class ResumesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.resumes'

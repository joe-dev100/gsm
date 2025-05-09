from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.models import signals


class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'category'
    
    def ready(self):
        import category.signals
        # from django.db.models.signals import post_migrate

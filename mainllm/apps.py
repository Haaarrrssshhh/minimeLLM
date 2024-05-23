# mainllm/apps.py
from django.apps import AppConfig

class MainllmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainllm'

    def ready(self):
        print("here 1")
        from .signals import initialize_embeddings
        initialize_embeddings()

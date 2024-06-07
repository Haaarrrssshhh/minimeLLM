# mainllm/apps.py
from django.apps import AppConfig

class MainllmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        print("here 1")
        from .chromadb_client import chromadbclient
        chromadbclient()

from django.urls import path
from .views import QueryView

urlpatterns = [
    path('api/query/', QueryView.as_view(), name='query')
]

from django.urls import path
from .views import ElasticsearchView


urlpatterns = [
    path('elastic/', ElasticsearchView.as_view(), name='elastic-create'),
    path('elastic/<int:pk>/', ElasticsearchView.as_view(), name='elastic-detail'),
]

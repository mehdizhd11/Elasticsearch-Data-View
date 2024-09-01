from django.urls import path
from .views import *


urlpatterns = [
    path('elastic-charts/range-view/<int:pk>/', ElasticsearchRangeView.as_view(), name='elastic-charts-range-view'),
]

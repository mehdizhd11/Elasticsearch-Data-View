from django.urls import path
from .views import *


urlpatterns = [
    path('elastic-charts/range-view/<int:pk>/', RangeView.as_view(), name='elastic-charts-range-view'),
    path('elastic-charts/complete-view/<int:pk>/', CompleteView.as_view(), name='elastic-charts-complete-view'),
]

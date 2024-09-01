from rest_framework import serializers
from .models import *


class ElasticsearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elasticsearch
        fields = '__all__'

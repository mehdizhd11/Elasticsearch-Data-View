from rest_framework import serializers
from .models import *


class ElasticsearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElasticConfig
        fields = '__all__'

from rest_framework.views import APIView
from .models import ElasticConfig
from .serializers import ElasticsearchSerializer
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class ElasticsearchView(APIView):

    def post(self, request):
        try:
            serializer = ElasticsearchSerializer(data=request.data)
            if serializer.is_valid():
                if ElasticConfig.objects.filter(**serializer.validated_data).exists():
                    message = {'status': 'ERROR', 'data': 'ElasticConfig already exists'}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                message = {'status': 'CREATED', 'data': serializer.data}
                return Response(message, status=status.HTTP_201_CREATED)
            else:
                message = {'status': 'ERROR', 'data': serializer.errors}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message = {'status': 'ERROR', 'data': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk):
        try:
            elastic = get_object_or_404(ElasticConfig, pk=pk)
            serializer = ElasticsearchSerializer(elastic)
            message = {'status': 'GET', 'data': serializer.data}
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = {'status': 'ERROR', 'data': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        try:
            elastic = get_object_or_404(ElasticConfig, pk=pk)
            serializer = ElasticsearchSerializer(elastic, data=request.data)
            if serializer.is_valid():
                serializer.save()
                message = {'status': 'UPDATED', 'data': serializer.data}
                return Response(message, status=status.HTTP_200_OK)
            else:
                message = {'status': 'ERROR', 'data': serializer.errors}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message = {'status': 'ERROR', 'data': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            elastic = get_object_or_404(ElasticConfig, pk=pk)
            elastic.delete()
            message = {'status': 'DELETED', 'data': pk}
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            message = {'status': 'ERROR', 'data': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

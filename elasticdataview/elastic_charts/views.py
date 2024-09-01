from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from elastic.models import ElasticConfig
from elasticsearch import Elasticsearch


class ElasticsearchRangeView(APIView):

    def get(self, request, pk):
        try:
            es_config = get_object_or_404(ElasticConfig, pk=pk)
            es = Elasticsearch(
                [es_config.host],
                http_auth=(es_config.username, es_config.password),
                verify_certs=True,
            )

            query_params = request.query_params.dict()

            index = query_params.get("index")
            field = query_params.get("field")
            start = query_params.get("start")
            end = query_params.get("end")

            query = {
                "range": {
                    field: {
                        "gte": start,
                        "lte": end
                    }
                }
            }

            data = es.search(index=index, body=query)

            print(data)

            return Response({"OK"})
        except Exception as e:
            message = {'status': 'ERROR', 'message': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from elastic.models import ElasticConfig
from elasticsearch import Elasticsearch


class CompleteView(APIView):

    def get(self, request, pk):
        try:
            es_config = ElasticConfig.objects.get(pk=pk)
            es = Elasticsearch(
                [es_config.host],
                http_auth=(es_config.username, es_config.password),
                verify_certs=False,
            )

            body = {
                "query": {
                    "match_all": {}
                }
            }

            query_params = request.query_params.dict()
            index = query_params.get("index")

            data = es.search(index=index, body=body, scroll='1m', size=10000)
            scroll_id = data['_scroll_id']

            response_data = [hit['_source'] for hit in data['hits']['hits']]

            while len(data['hits']['hits']) > 0:
                data = es.scroll(scroll_id=scroll_id, scroll='1m')
                scroll_id = data['_scroll_id']
                response_data.extend(hit['_source'] for hit in data['hits']['hits'])

            es.clear_scroll(scroll_id=scroll_id)

            message = {'status': 'OK', "length": len(response_data), 'data': response_data}
            return Response(message, status=status.HTTP_200_OK)

        except Exception as e:
            message = {'status': 'ERROR', 'message': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class RangeView(APIView):

    def get(self, request, pk):
        try:
            es_config = get_object_or_404(ElasticConfig, pk=pk)
            es = Elasticsearch(
                [es_config.host],
                http_auth=(es_config.username, es_config.password),
                verify_certs=False,
            )

            query_params = request.query_params.dict()

            index = query_params.get("index")
            field = query_params.get("field")
            gte = query_params.get("start")
            lte = query_params.get("end")

            body = {
                "query": {
                    "range": {
                        field: {
                            "gte": gte,
                            "lte": lte,
                        }
                    }
                }
            }

            data = es.search(index=index, body=body, scroll='1m', size=10000)
            scroll_id = data['_scroll_id']

            response_data = [hit['_source'] for hit in data['hits']['hits']]

            while len(data['hits']['hits']) > 0:
                data = es.scroll(scroll_id=scroll_id, scroll='1m')
                scroll_id = data['_scroll_id']
                response_data.extend(hit['_source'] for hit in data['hits']['hits'])

            es.clear_scroll(scroll_id=scroll_id)

            message = {'status': 'OK', "length": len(response_data), 'data': response_data}
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = {'status': 'ERROR', 'message': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class AggregationView(APIView):

    def get(self, request, pk):
        try:
            es_config = get_object_or_404(ElasticConfig, pk=pk)
            es = Elasticsearch(
                [es_config.host],
                http_auth=(es_config.username, es_config.password),
                verify_certs=False,
            )

            query_params = request.query_params.dict()
            index = query_params.get("index")
            field = query_params.get("field")

            body = {
                "aggs": {
                    "agg_result": {
                        "terms": {
                            "field": field,
                            "size": 10000,
                        }
                    }
                }
            }

            data = es.search(index=index, body=body)
            agg_result = data['aggregations']['agg_result']['value']

            message = {'status': 'OK', 'aggregation_result': agg_result}
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = {'status': 'ERROR', 'message': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class TermQueryView(APIView):

    def get(self, request, pk):
        try:
            es_config = get_object_or_404(ElasticConfig, pk=pk)
            es = Elasticsearch(
                [es_config.host],
                http_auth=(es_config.username, es_config.password),
                verify_certs=False,
            )

            query_params = request.query_params.dict()
            index = query_params.get("index")
            field = query_params.get("field")
            value = query_params.get("value")

            body = {
                "query": {
                    "term": {
                        field: value
                    }
                }
            }

            data = es.search(index=index, body=body, scroll='1m', size=10000)
            scroll_id = data['_scroll_id']

            response_data = [hit['_source'] for hit in data['hits']['hits']]

            while len(data['hits']['hits']) > 0:
                data = es.scroll(scroll_id=scroll_id, scroll='1m')
                scroll_id = data['_scroll_id']
                response_data.extend(hit['_source'] for hit in data['hits']['hits'])

            es.clear_scroll(scroll_id=scroll_id)

            message = {'status': 'OK', "length": len(response_data), 'data': response_data}
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = {'status': 'ERROR', 'message': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

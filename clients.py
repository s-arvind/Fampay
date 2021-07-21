from datetime import datetime

from dateutil.relativedelta import relativedelta
from elasticsearch import AsyncElasticsearch
from elasticsearch import helpers
from googleapiclient.discovery import build
from requests import HTTPError
from loguru import logger
from config import *
from pymongo import MongoClient
import sys

logger.configure(**{'handlers': [{'sink': sys.stdout, 'enqueue': True}]})

__all__ = ('youtube_client', 'es_client', 'mongo_client', 'logger')


class Youtube:

    def __init__(self):
        self.key = mongo_client.get_key()
        self.client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=self.key['key'])

    async def search(self):
        try:
            query = {}
            es_client.query_builder({}, 1, 0, query)
            publish_time = (datetime.now() + relativedelta(hours=-6)).strftime('%Y-%m-%dT%H:%M:%SZ')
            es_response = await es_client.search(query)
            if es_response.get('hits') and es_response['hits'].get('hits'):
                record = es_response['hits'].get('hits')[0]
                publish_time = record['_source']['publishedAt']
            response = self.client.search().list(
                part="id,snippet",
                order="date",
                relevanceLanguage="en",
                type="video",
                publishedAfter=publish_time,
                maxResults=50,
            ).execute()

            if response['items']:
                await es_client.insert(response['items'])
        except HTTPError as E:
            mongo_client.update(self.key['_id'])
        except Exception as E:
            logger.info(str(E))


class ElasticSearch:

    def __init__(self, host, port):
        self.client = AsyncElasticsearch(
            [f'{host}:{port}'],
        )

    @staticmethod
    async def process_record(items):
        for item in items:
            yield {
                "_index": ES_INDEX,
                '_id': item['id']['videoId'],
                "_source": {
                    'type': item['id']['kind'].split('#')[-1],
                    'publishedAt': item['snippet']['publishedAt'],
                    'channelId': item['snippet']['channelId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'thumbnails': item['snippet']['thumbnails'],
                    'channelTitle': item['snippet']['channelTitle']
                }
            }

    @staticmethod
    def query_builder(filters, limit, skip, query):
        must_query = []
        if filters.get('q'):
            must_query.append({
                'multi_match': {
                    'query': filters['q'],
                    'fields': ['title', 'description'],
                    'fuzziness': 'AUTO'
                }
            })
        if filters.get('type'):
            must_query.append({
                'term': {
                    'type': filters['type']
                }
            })
        if filters.get('publish_after'):
            must_query.append({
                'range': {
                    'publishedAt': {
                        "gt": filters['publish_after']
                    }
                }
            })
        if filters.get('channel'):
            must_query.append({
                'match': {
                    'channelTitle': filters['channel']
                }
            })
        if len(must_query) > 0:
            query.update({
                'query': {
                    'bool': {
                        'must': must_query
                    }
                }
            })

        query.update({
            'sort': [
                {'publishedAt': 'desc'}
            ],
            'size': limit,
            'from': skip
        })

    async def insert(self, items):
        await helpers.async_bulk(self.client, self.process_record(items))

    async def search(self, query):
        es_response = await self.client.search(index=ES_INDEX, body=query)
        return es_response


class MongoDb:

    def __init__(self, host, port, db):
        self.client = MongoClient(host, int(port))
        self.db = self.client[db]

    def get_key(self):
        key = self.db.youtube_keys.find_one({'is_expired': False})
        return key

    def update(self, id):
        self.db.update_one({'_id': id}, {'$set': {'is_expired': True}})


youtube_client = Youtube()
es_client = ElasticSearch(ES_HOST, ES_PORT)
mongo_client = MongoDb(MONGO_HOST, int(MONGO_PORT), MONGO_DB)




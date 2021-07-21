from decouple import config

DEVELOPER_KEY = config('DEVELOPER_KEY')
YOUTUBE_API_SERVICE_NAME = config('YOUTUBE_API_SERVICE_NAME', 'youtube')
YOUTUBE_API_VERSION = config('YOUTUBE_API_VERSION', 'v3')
MONGO_HOST = config('MONGO_HOST')
MONGO_PORT = config('MONGO_PORT')
MONGO_DB = config('MONGO_DB')
ES_HOST = config('ES_HOST')
ES_PORT = config('ES_PORT')
ES_INDEX = config('ES_INDEX')
CRON_TIME = config('CRON_TIME')
WORKERS = config('WORKERS')

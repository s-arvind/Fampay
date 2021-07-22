Search API Redoc

    `{Host}/api/redoc`

Tech Stack
1. Python
2. FastAPI
3. Elasticsearch
4. Mongodb
5. docker

Development:

create `.env` file inside `Fampay` directory

    DEVELOPER_KEY=YOUTUBE_DEVELOPER_KEY
    YOUTUBE_API_SERVICE_NAME=youtube
    YOUTUBE_API_VERSION=v3
    MONGO_HOST=localhost
    MONGO_PORT=27017
    MONGO_DB=fampay
    ES_HOST=localhost
    ES_PORT=9200
    ES_INDEX=youtube
    CRON_TIME=10
    WORKERS=2

install `docker`

To run `mongodb`, `elasticsearch` and `kibana` separately

    docker run -p 27017:27017 -it -v mongodata:/data/db --name mongodb -d mongo
    docker run --name es01-test --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.4
    docker run --name kib01-test --net elastic -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://es01-test:9200" docker.elastic.co/kibana/kibana:7.13.4    

create elasticsearch index:
    go to  `http://localhost:5601/app/dev_tools#/console` and run:

    PUT youtube
    {
      "settings": {
        "analysis": {
          "filter": {
            "autocomplete_filter": {
              "type": "edge_ngram",
              "min_gram": 1,
              "max_gram": 20
            }
          },
          "analyzer": {
            "autocomplete": { 
              "type": "custom",
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "autocomplete_filter"
              ]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "title": {
            "type": "text",
            "analyzer": "autocomplete", 
            "search_analyzer": "standard" 
          },
          "description": {
            "type": "text",
            "analyzer": "autocomplete", 
            "search_analyzer": "standard" 
          },
          "channelTitle": {
            "type": "text",
            "analyzer": "autocomplete", 
            "search_analyzer": "standard" 
          },
          "publishedAt": {
            "type": "date"
          }
        }
      }
    }


create mongodb database `fampay` and collection `youtube_keys` and insert records
    
    {
        "key": "YOUTUBE DEVELOPER KEY",
        "is_expired": False
    }


install `python3.9` and install `poetry` 

    `curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python `

Go to Fampay directory and install packages with poetry

    cd {HOME}/Fampay/
    poetry install

run app server
    
    poetry run python -m main.py

to sync records

    poetry run python -m cron_script.sync_data

To run with docker-compose

    docker-compose up -d
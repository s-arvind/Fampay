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


Example:

`GET  http://localhost:8000/api/search?q=ntervie`
Response:

    {
    "count": 1,
    "data": [
            {
                "type": "video",
                "publishedAt": "2021-07-21T19:50:54+00:00",
                "channelId": "UC8CbFnDTYkiVweaz8y9wd_Q",
                "title": "Paul Duncan Interview Star Wars Archives and George Lucas - Rule of Two",
                "description": "Todays is another special day on Rule of Two where we get to speak with Paul Duncan. Paul Duncan is a film historian whose TASCHEN books include The ...",
                "thumbnails": {
                    "default": {
                        "url": "https://i.ytimg.com/vi/eoBIha9zk28/default.jpg",
                        "width": 120,
                        "height": 90
                    },
                    "medium": {
                        "url": "https://i.ytimg.com/vi/eoBIha9zk28/mqdefault.jpg",
                        "width": 320,
                        "height": 180
                    },
                    "high": {
                        "url": "https://i.ytimg.com/vi/eoBIha9zk28/hqdefault.jpg",
                        "width": 480,
                        "height": 360
                    }
                },
                "channelTitle": "Star Wars Theory"
            }
        ]
    }
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from clients import es_client
from schemas import Pagination, SearchSchema, SearchResponse, ErrorMessage

router = APIRouter()


@router.get('/search', response_model=SearchResponse,
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorMessage}})
async def search(request: SearchSchema = Depends(), pagination: Pagination = Depends()):
    """ search api for youtube data"""
    request_dict = request.dict(by_alias=True, skip_defaults=True)
    query = {}
    try:
        es_client.query_builder(request_dict, pagination.limit, pagination.skip, query)
        data = await es_client.search(query)
        response = {
            'count': data['hits']['total']['value'],
            'data': []
        }
        for item in data['hits']['hits']:
            record = {'_id': item['_id']}
            record.update(item['_source'])
            response['data'].append(record)
    except Exception as E:
        return JSONResponse({'message': str(E)})
    return response, status.HTTP_200_OK

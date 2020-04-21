import logging
import json
import time
import asyncio
import aiohttp
import azure.functions as func
from ..shared.mainProc import processMain 
from ..shared.common import time_convert

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    start_time = time.time()

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        await processMain(req_body, logging)
        end_time = time.time()
        time_lapsed = end_time - start_time
        logging.info('Function completed in: ' + str(time_convert(time_lapsed)))
        return func.HttpResponse(
             "Success",
             status_code=200
        )
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )

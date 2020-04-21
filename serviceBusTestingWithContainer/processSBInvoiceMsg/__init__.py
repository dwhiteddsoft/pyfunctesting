import logging
import json
import time 
import asyncio
import azure.functions as func
from ..shared.mainProc import processMain 
from ..shared.common import time_convert

async def main(msg: func.ServiceBusMessage, context: func.Context):
    logging.info('Python ServiceBus queue trigger processed message: %s',
                 msg.get_body().decode('utf-8'))
    start_time = time.time()
    message = json.loads(msg.get_body().decode('utf-8'))
    await processMain(message, logging)
    end_time = time.time()
    time_lapsed = end_time - start_time
    logging.info('Function completed in: ' + str(time_convert(time_lapsed)))
    logging.info('function completed')

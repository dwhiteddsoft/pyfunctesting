import logging
import json
import azure.functions as func
from ..shared.mainProc import processMain 

async def main(msg: func.ServiceBusMessage, context: func.Context):
    logging.info('Python ServiceBus queue trigger processed message: %s',
                 msg.get_body().decode('utf-8'))
    message = json.loads(msg.get_body().decode('utf-8'))
    processMain(message, logging)
    logging.info('function completed')

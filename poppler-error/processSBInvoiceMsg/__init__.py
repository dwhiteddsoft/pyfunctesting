import logging
import io
import os
import time
import json
import azure.functions as func
from PIL import Image
from pdf2image import convert_from_bytes
from azure.storage.blob import BlobClient
from ..shared.data_processing import image_to_text

def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format="PNG")
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  precision = 4
  sec2 = "{:.{}f}".format( sec, precision )
  return "Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec2)

async def main(msg: func.ServiceBusMessage, context: func.Context):
    logging.info('Python ServiceBus queue trigger processed message: %s',
                 msg.get_body().decode('utf-8'))
    message = json.loads(msg.get_body().decode('utf-8'))

    #check storage option
    storageConnectionString = os.environ["Invoice_Storage_Connection_String"]
    storageContainer = os.environ["Invoice_Storage_Container"]

    #check output option
    outputConnectionString = os.environ["Invoice_Output_Storage_Connection_String"]
    outputStorageContainer = os.environ["Invoice_Output_Storage_Container"]

    fileName = message['name']
    blobIn = BlobClient.from_connection_string(conn_str=storageConnectionString, container_name=storageContainer, 
        blob_name=fileName)
    start_time = time.time()
    blob_data = blobIn.download_blob()
    end_time = time.time()
    time_lapsed = end_time - start_time
    logging.info('Download Azure BLOB completed in: ' + str(time_convert(time_lapsed)))

    start_time = time.time()
    images = convert_from_bytes(blob_data.readall(), dpi=300)
    end_time = time.time()
    time_lapsed = end_time - start_time
    logging.info('Image conversion completed in: ' + str(time_convert(time_lapsed)))
    imgByteArray = image_to_byte_array(images[0])
    logging.info('Image bytes: ' + str(len(imgByteArray)))

    outputName = fileName.rsplit( ".", 1 )[ 0 ]  
    outputImage = 'img/' + outputName + '.png'  
    outputOCR = 'ocr/' + outputName + '.json'  
    outputhOCR = 'hOCR/' + outputName + '.xml'  

    blobOutImage = BlobClient.from_connection_string(conn_str=outputConnectionString, container_name=outputStorageContainer, 
        blob_name=outputImage)
    start_time = time.time()
    blobOutImage.upload_blob(imgByteArray, blob_type="BlockBlob", length=len(imgByteArray), overwrite=True, timeout=1200)    
    end_time = time.time()
    time_lapsed = end_time - start_time
    logging.info('Upload of image to Azure BLOB completed in: ' + str(time_convert(time_lapsed)))

    #process OCR
    start_time = time.time()
    data = image_to_text(
        images[0],
        resize_max_size=2500,
        fix_orientation=True)
    blobOutOcr = BlobClient.from_connection_string(conn_str=outputConnectionString, container_name=outputStorageContainer, 
        blob_name=outputOCR)
    blobOutOcr.upload_blob(json.dumps(data['text']), blob_type="BlockBlob", overwrite=True)
    end_time = time.time()
    time_lapsed = end_time - start_time
    logging.info('Upload of OCR to Azure BLOB completed in: ' + str(time_convert(time_lapsed)))

    #process hOCR
    start_time = time.time()
    data_hocr = image_to_text(
        images[0],
        resize_max_size=2500,
        hocr=True,
        fix_orientation=True)
    blobOuthOCR = BlobClient.from_connection_string(conn_str=outputConnectionString, container_name=outputStorageContainer, 
        blob_name=outputhOCR)
    blobOuthOCR.upload_blob(data_hocr, blob_type="BlockBlob", overwrite=True)
    end_time = time.time()
    time_lapsed = end_time - start_time
    logging.info('Upload of hOCR to Azure BLOB completed in: ' + str(time_convert(time_lapsed)))
    logging.info('function completed')

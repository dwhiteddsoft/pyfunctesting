import io
import os
import time
import json
import asyncio
from PIL import Image
from pdf2image import convert_from_bytes
#from azure.storage.blob import BlobClient
from azure.storage.blob.aio import BlobServiceClient
from ..shared.data_processing import image_to_text
from .common import time_convert

def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format="PNG")
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

async def uploadFiletoBLOB(blob_service_client:BlobServiceClient, outputConnectionString, outputStorageContainer, fileName, data, logging):
    logging.info('uploadFiletoBLOB started with: ' + fileName)
    start_time = time.time()
    blobClientUpload = blob_service_client.get_blob_client(outputStorageContainer, fileName)
    await blobClientUpload.upload_blob(data, blob_type="BlockBlob", length=len(data), overwrite=True, timeout=1200)
    end_time = time.time()
    time_lapsed = end_time - start_time
    await blobClientUpload.close()
    logging.info('Upload ' + fileName + ' to Azure BLOB completed in: ' + str(time_convert(time_lapsed)))

async def processMain(message, logging):
    #check storage option
    storageConnectionString = os.environ["Invoice_Storage_Connection_String"]
    storageContainer = os.environ["Invoice_Storage_Container"]

    #check output option
    outputConnectionString = os.environ["Invoice_Output_Storage_Connection_String"]
    outputStorageContainer = os.environ["Invoice_Output_Storage_Container"]

    blob_service_client = BlobServiceClient.from_connection_string(storageConnectionString)
    
    fileName = message['name']
    blobIn = blob_service_client.get_blob_client(storageContainer, fileName)
    start_time = time.time()
    blob_data = await blobIn.download_blob()
    end_time = time.time()
    time_lapsed = end_time - start_time
    await blob_service_client.close()
    logging.info('Download Azure BLOB completed in: ' + str(time_convert(time_lapsed)))

    start_time = time.time()
    input = await blob_data.readall()
    images = convert_from_bytes(input, dpi=300)
    end_time = time.time()
    time_lapsed = end_time - start_time
    logging.info('Image conversion completed in: ' + str(time_convert(time_lapsed)))
    imgByteArray = image_to_byte_array(images[0])
    logging.info('Image bytes: ' + str(len(imgByteArray)))

    outputName = fileName.rsplit( ".", 1 )[ 0 ]  
    outputImage = 'img/' + outputName + '.png'  
    outputOCR = 'ocr/' + outputName + '.json'  
    outputhOCR = 'hOCR/' + outputName + '.xml'  

    #process OCR
    data = image_to_text(
        images[0],
        resize_max_size=2500,
        fix_orientation=True)

    #process hOCR
    data_hocr = image_to_text(
        images[0],
        resize_max_size=2500,
        hocr=True,
        fix_orientation=True)

    blob_service_client = BlobServiceClient.from_connection_string(outputConnectionString)
    await asyncio.gather(
        uploadFiletoBLOB(blob_service_client,outputConnectionString,outputStorageContainer,outputImage,imgByteArray, logging),
        uploadFiletoBLOB(blob_service_client,outputConnectionString,outputStorageContainer,outputOCR,json.dumps(data['text']), logging),
        uploadFiletoBLOB(blob_service_client,outputConnectionString,outputStorageContainer,outputhOCR,data_hocr, logging)
    )
    await blob_service_client.close()


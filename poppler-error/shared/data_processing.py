import json
import os
import tempfile
import traceback

import pdf2image
import pytesseract
# from matplotlib import pyplot as plt
# from PyPDF2 import PdfFileReader
from pytesseract import Output, TesseractError
from .common import get_image, resize_with_aspect_ratio

def image_to_text(
        image,
        resize_max_size=2800,
        fix_orientation=True,
        return_image=False,
        hocr=False,
        save_output=False,
        output_file=None,
        continue_on_error=True,
        verbose=1):
    """[summary]
    
    Args:
        image ([type]): [description]
        resize_max_size (int, optional): [description]. Defaults to 2800.
        fix_orientation (bool, optional): [description]. Defaults to True.
        return_image (bool, optional): [description]. Defaults to False.
        hocr (bool, optional): [description]. Defaults to False.
        save_output (bool, optional): [description]. Defaults to False.
        output_file ([type], optional): [description]. Defaults to None.
        continue_on_error (bool, optional): [description]. Defaults to True.
        verbose (int, optional): [description]. Defaults to 1.
    
    Raises:
        e: [description]
    
    Returns:
        [type]: [description]
    """
    if verbose == 2:
        print("===============")
        print("Processing image: ", image)
    try:
        pil_im = get_image(image)
        if resize_max_size is not None:
            pil_im = resize_with_aspect_ratio(pil_im, resize_max_size)
            if verbose == 2:
                print("Resized image to max size: ", resize_max_size)
                print("Output size: ", pil_im.size)
        if fix_orientation:   
            osd = pytesseract.image_to_osd(pil_im, output_type=Output.DICT)
            rotation = osd['orientation']
            if rotation > 0:
                pil_im = pil_im.rotate(rotation, expand=True)
            if verbose == 2:
                print("Rotated image by: ", rotation)
        data = None
        output_ext = ".json"
        if hocr:
            data = pytesseract.image_to_pdf_or_hocr(
                pil_im, lang='eng', extension='hocr')
            output_ext = ".xml"
        else:
            data = pytesseract.image_to_data(
                pil_im, lang='eng',
                output_type=Output.DICT)
            if fix_orientation:
                data['osd'] = osd
            output_ext = ".json"
        if (output_file is not None or (type(image) is str)) and save_output:
            output_file = output_file if output_file is not None else image
            # ensure propper extension
            output_file = os.path.splitext(output_file)[0] + output_ext
            # I was getting weird error and replacing slashes helped so:
            output_file = output_file.replace(
                "\\", "/").replace("\\", "/")
            with open(output_file, 'wb') as file_object:
                if hocr:
                    file_object.write(data)
                else:
                    # Save dict data into the JSON file.
                    json.dump(data, file_object)
                if verbose == 2:
                    print("Saved OCR to output file:", output_file)
        elif save_output:
            if verbose == 2:
                print(("Saving output was requested but output file path was not provided.\n"  # NOQA E501
                        "Please provide correct path as `output_file` param."))
        if return_image:
            if verbose == 2:
                print("Returning complete OCR data + processed PIL Image..")
            return data, pil_im
        else:
            if verbose == 2:
                print("Returning complete OCR data..")
            return data
    except Exception as e:
        if not continue_on_error:
            raise e
        if verbose > 0:
            print('--------------------------------------')
            print('Error caught while processing: ', image)
            print('Returning empty string!')
            print('+++')
            print('Error msg:', e)
            print('Error traceback: \n\n', traceback.format_exc())
            print('--------------------------------------')
        if return_image:
            return "", None
        else:
            return ""
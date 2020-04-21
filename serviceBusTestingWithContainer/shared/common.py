from PIL import Image
from PIL.PngImagePlugin import PngImageFile
from PIL.PpmImagePlugin import PpmImageFile


def get_image(image, clr_mode='L'):
    assert(clr_mode in ['L', 'RGB'])
    image_type = type(image)
    pil_im = None

    if image_type is str:
        pil_im = Image.open(image).convert(clr_mode)
    elif image_type in [PngImageFile, Image.Image, Image, PpmImageFile]:
        pil_im = image.convert(clr_mode)
    else:
        raise ValueError("Unsupported type of input image argument")

    return pil_im


def resize_with_aspect_ratio(img, max_size=2800):
    w, h = img.size
    aspect_ratio = min(max_size/w, max_size/h)
    resized_img = img.resize(
        (int(w * aspect_ratio), int(h * aspect_ratio))
    )
    return resized_img

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  precision = 4
  sec2 = "{:.{}f}".format( sec, precision )
  return "Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec2)


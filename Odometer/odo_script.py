import cv2
import torch
import easyocr
import re
from ultralytics import YOLO
from pathlib import Path

# def load_model(path):
#     return YOLO(path)


# def pred_img(model, img, device='cpu'):
#     pred = model.predict(img, save=False, device=device)
#     boxes=pred[0].boxes.data.cpu().numpy()
#     return boxes
     

# def ocr(img, box, cuda=False):
#     if len(box) != 1:
#         return ''
#     image = cv2.imread(img)
#     x1, y1, x2, y2, _, _ = map(int, box[0])
#     cropped = image[y1:y2, x1:x2]
#     gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
#     reader = easyocr.Reader(['en'], gpu=cuda)
#     res = reader.readtext(gray, detail=0)
#     text = " ".join(res)
#     result = re.sub(r'[^0-9]', '', text)
#     return result


# def pipeline(path, img):
#     cuda = torch.cuda.is_available()
#     device = "cuda" if cuda else "cpu"
    
#     model = load_model(path)
#     boxes = pred_img(model, img, device)
#     num = ocr(img, boxes, cuda)
#     if num:
#         return num
#     return ''

# path = r'Odometer\odo_model.pt'
# img = r'Odometer\test_img\odo1.jpg'

# res = pipeline(path, img)
# print("Odometer Reading: ", res)


# =================================================================== #
#                             FOR FLASK                               #
# =================================================================== #
script_dir = Path(__file__).resolve().parent

# Load the model
model = YOLO(str(script_dir/'odo_model.pt'))

def pipeline(img):
    """
    Process the odometer image to extract the mileage reading.
    """
    cuda = torch.cuda.is_available()
    device = "cuda" if cuda else "cpu"

    boxes = model.predict(img, save=False, device=device)[0].boxes.data.cpu().numpy()
    if len(boxes) != 1:
        return '0'

    x1, y1, x2, y2, _, _ = map(int, boxes[0])
    image = cv2.imread(img)
    cropped = image[y1:y2, x1:x2]
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    reader = easyocr.Reader(['en'], gpu=cuda)
    res = reader.readtext(gray, detail=0)
    text = " ".join(res)
    result = re.sub(r'[^0-9]', '', text)

    return result if result else '0'
import dlib
from PIL import Image
import skimage
import numpy as np
from skimage import io
from deskew2 import Deskew
from io import BytesIO
import importlib
import requests
import azure.storage.blob
importlib.reload(azure.storage.blob)
from azure.storage.blob import BlockBlobService

def blobsave(imgbyte,name):
    try:
        block_blob_service = BlockBlobService(account_name='tbgonboarding', account_key='o9oQ1XdVZPaaAy4oD4XsFHSTYRF/z2Mz35aCuxjh3PNCq+a2A+XBbUH7lunww4462ETsVZnOPTGSNjI10hakPA==')
        container_name ='documents'
        name=name+"_face"
        block_blob_service.create_blob_from_bytes(container_name,name+".jpg",imgbyte)
        return 1
    except:
        return 0

def detect_faces(image):

    # Create a face detector
    face_detector = dlib.get_frontal_face_detector()

    # Run detector and get bounding boxes of the faces on image.
    detected_faces = face_detector(image, 1)
    
    face_frames = [(x.left(), x.top(),
                    x.right(), x.bottom()) for x in detected_faces]
    
    return face_frames

def extract_face(img_data,name):
    try:
        image=io.imread(BytesIO(img_data))
#        return image
#        io.imsave("a.jpg",image)
        _,_,a=image.shape
        if a==4:
            image=(skimage.color.rgba2rgb(image)*255).astype(np.uint8)
        elif a<3:
            return 5
        d=detect_faces(image)
    except:
        return 4
    
    if len(d)==0:
        deskew_obj = Deskew(image,"a","b")
        image_rot=deskew_obj.run()
        
        d=detect_faces(image_rot)
    
        if len(d)==0:
            deskew_obj = Deskew(image,"a","b", r_angle=180)
            image_rot=deskew_obj.run()
            d=detect_faces(image_rot)
            
            if len(d)==0:
#                return "No Face Found"
                return 3
            
    d2=[(d[0][0]-10,d[0][1]-15,d[0][2]+10,d[0][3]+20)]
    try:
        for n, face_rect in enumerate(d2):
            face = Image.fromarray(image_rot).crop(face_rect)
            imgByteArr = BytesIO()
            face.save(imgByteArr, format='PNG')
            imgByteArr = imgByteArr.getvalue()
            return blobsave(imgByteArr,name)
    except:
        for n, face_rect in enumerate(d2):
            face = Image.fromarray(image).crop(face_rect)
            imgByteArr = BytesIO()
            face.save(imgByteArr, format='PNG')
            imgByteArr = imgByteArr.getvalue()
            return blobsave(imgByteArr,name)
            

# Load image
if __name__=='__main__':
    img_path = 'Balaji Eepa.jpg'
#    img_path='kp1f.jpg'
    with open(img_path, "rb") as f:
        img_data = f.read()
#    img="https://tbgonboarding.blob.core.windows.net/documents/Balaji Eepa.jpg"
#    response = requests.get(img)
#    img_data=response.content
    a=extract_face(img_data,"lols")


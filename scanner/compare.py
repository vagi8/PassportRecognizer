import face_recognition
import cv2
import requests
from skimage import io
from io import BytesIO

def comparefaces(img1,frames):
    try:
        known_image=io.imread(BytesIO(img1))
    except:
        return 0
#    unknown_image=io.imread(BytesIO(img2))
#    known_image=img1
    for i in frames:
        unknown_image=i
        try:
            img1_encoding = face_recognition.face_encodings(known_image)[0]
            img2_encoding = face_recognition.face_encodings(unknown_image)[0]
        except:
            continue
        face_distances = face_recognition.face_distance([img1_encoding], img2_encoding)
        print(face_distances)
        if face_distances<0.5:
            return 1
    return 0

def compare(img,vid_path):
    cap = cv2.VideoCapture(vid_path)
    #fps = cap.get(cv2.CAP_PROP_FPS)
    #duration = frame_count/fps
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    topframes=[]
    for i in [0.3,0.5,0.8]:
        topframes.append(int(i*frame_count))
    
    success = 1
    count=0
    frames=[]
    while count<frame_count:
        if count in topframes:
            success, image = cap.read() 
            frames.append(image)
        count+=1
    response = requests.get(img)
    content_img=response.content
    
    
    a= comparefaces(content_img,frames)
#    return 1
    return a

if __name__=='__main__':
    vid="https://idpdocuments.blob.core.windows.net/documents/onboardingvideo.mp4"
    img="https://tbgonboarding.blob.core.windows.net/documents/akashOnboarding_face.jpg"
    img="https://tbgonboarding.blob.core.windows.net/documents/Akash Chatti_face.jpg"
    vid="C:\\Users\\vageeshan.mankala\\passport_re\\197url\\akashvid.mp4"
    a=compare(img,vid)
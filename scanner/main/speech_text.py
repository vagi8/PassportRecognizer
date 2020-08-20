import os 
import io
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:\\WebApps\\apikey_spech_to_text.json"
from moviepy.editor import VideoFileClip
import requests


def speech_to_text(vid_path,name,out_dir):
    videoclip = VideoFileClip(vid_path)
    vidconv_path=os.path.join(out_dir,name+'_audio.wav')
    videoclip.audio.write_audiofile(vidconv_path)
    videoclip.close()    
    
    client = speech_v1.SpeechClient()
    
    language_code = "en-US"
    sample_rate_hertz = 44100
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "audio_channel_count":2,
        "encoding": encoding,
    }
    
    with io.open(vidconv_path, "rb") as f:
        content = f.read()
    audio = {"content": content}
    
    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
    return alternative

if __name__=='__main__':
    vid_path="https://idpdocuments.blob.core.windows.net/documents/onboardingvideo.mp4"
    name='vageesh'
#    vid_content = requests.get(vid_path).content
    out_dir=os.path.join(app.instance_path, 'AppData')
    vid_local_path=os.path.join(out_dir,name+'.mp4')
#    with open(vid_local_path,"wb") as f:
#        f.write(vid_content)
    
    text=speech_to_text(vid_local_path,name,out_dir)
    
import json
from tqdm import tqdm
import utils
import io
import base64
import cv2
from PIL import Image
from langchain_google_genai import GoogleGenerativeAI
from langchain.schema import HumanMessage
from langchain.schema.messages import AIMessage, SystemMessage

llm = GoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0.8)
def process_chunk(images):
    frames={}
    for i, image in enumerate(images):
        img=cv2.resize(image, (256,144))
        buffer=io.BytesIO()
        img = Image.fromarray(img)
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        frame=base64.b64encode(buffer.read()).decode('utf-8')
        frames[f"frame {i}"] =frame
    final=json.dumps({"frames": frames})
    messages = [SystemMessage(content="your an AI integrated in to an audio description application. your job is to generate audio descriptions for the given video, wihch will be given to you as sequence of frames. each frame is given to you as base64 encoding string of a jpeg format. your job is to generate a detailed and accurate description of the video based on the frames. please make sure to include all relevant details and context in your description. note that we are not asking you frame wise description, but we are asking you to interpret the given sequence of frames as a video, interpret what is going on, and then generate a description of the video. please dont include frazes like here is the description, just jump in to the description, as the text which you will give is directly used in the audio describer application."), HumanMessage(content=final)]
    
    response = llm.invoke(messages)
    return response

def generate_description(video_path, start_frame=0, end_frame=None, threshold=0.75):
    video=cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise Exception("Could not open video file")
    framerate=video.get(cv2.CAP_PROP_FPS)
    print(f"Video framerate: {framerate}")
    framecount=int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames: {framecount}")
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    if end_frame is None:
        end_frame=framecount
    else:
        end_frame=min(end_frame, framecount)
    ret, frame = video.read()
    current_chunk=[frame]
    timestamp=start_frame/framerate
    descriptions=[]
    timestamps=[]
    
    print("Generating descriptions...")
    for i in tqdm(range(start_frame+1, end_frame)):
        ret, frame = video.read()
        if not ret:
            break
        if utils.check_similarity(frame, current_chunk[-1], threshold):
            current_chunk.append(frame)
        else:
            description=process_chunk(current_chunk)
            descriptions.append(description)
            timestamps.append(timestamp)
            current_chunk=[frame]
            timestamp=i/framerate
    if current_chunk:
        description=process_chunk(current_chunk)
        descriptions.append(description)
        timestamps.append(timestamp)
    video.release()
    return descriptions, timestamps

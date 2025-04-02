import json
from tqdm import tqdm
import utils
import io
import base64
from PIL import Image
from langchain_google_genai import GoogleGenerativeAI
from langchain.schema import HumanMessage
from langchain.schema.messages import AIMessage, SystemMessage

llm = GoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)

def process_chunk(images):
    frames={}
    for i, image in enumerate(images):
        buffer=io.BytesIO()
        img = Image.fromarray(image)
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        frame=base64.b64encode(buffer.read()).decode('utf-8')
        frames[f"frame {i}"] =frame
    final=json.dumps({"frames": frames})
    messages = [SystemMessage(content="your an AI integrated in to an audio description application. your job is to generate audio descriptions for the given video, wihch will be given to you as sequence of frames. each frame is given to you as base64 encoding string of a jpeg format. your job is to generate a detailed and accurate description of the video based on the frames. please make sure to include all relevant details and context in your description. note that we are not asking you frame wise description, but we are asking you to interpret the given sequence of frames as a video, interpret what is going on, and then generate a description of the video. please dont include frazes like here is the description, just jump in to the description, as the text which you will give is directly used in the audio describer application."), HumanMessage(content=final)]
    
    response = llm.invoke(messages)
    return response

def generate_description(video_path, start_frame=0, end_frame=None):
    # Load the video and extract frames
    video_path = video_path
    frames, framerate = utils.load_video(video_path, start_frame, end_frame)
    
    # Split the frames into chunks based on temporal similarity
    chunks, timestamps = utils.make_chunks(frames, framerate)
    descriptions=[]
    
    # Process each chunk and generate descriptions
    print("Generating descriptions...")
    for i, chunk in tqdm(enumerate(chunks)):
        description = process_chunk(chunk)
        descriptions.append(description)
    return descriptions, timestamps

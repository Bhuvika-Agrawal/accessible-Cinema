import json
import utils
from langchain_google_genai import GoogleGenerativeAI
from langchain.schema import HumanMessage
from langchain.schema.messages import AIMessage, SystemMessage

llm = GoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)

def process_chunk(images):
    frames={}
    for i, image in enumerate(images):
        # Assuming images are in a list and you want to create a dictionary with keys as indices
        frames[f"frame {i}"] = image.tolist() 
    final=json.dumps({"frames": frames})
    messages = [SystemMessage(content="your an AI integrated in to an audio description application. your job is to generate audio descriptions for the given video, wihch will be given to you as sequence of images. you will be given a prompt, which will be the audio description of the video. your job is to generate a detailed and accurate description of the video based on the images and the prompt. please make sure to include all relevant details and context in your description."), HumanMessage(content=final)]
    
    response = llm.invoke(messages)
    return response

def generate_description(video_path, start_frame=0, end_frame=None):
    # Load the video and extract frames
    video_path = 'video.mp4'
    frames, framerate = utils.load_video(video_path, start_frame, end_frame)
    
    # Split the frames into chunks based on temporal similarity
    chunks, timestamps = utils.make_chunks(frames, framerate)
    descriptions=[]
    
    # Process each chunk and generate descriptions
    for i, chunk in enumerate(chunks):
        description = process_chunk(chunk)
        descriptions.append(description)
